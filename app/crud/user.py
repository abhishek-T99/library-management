from typing import Any, List

from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.db.models import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.exceptions import UserNotFoundException, InvalidCredentialsException, UserLockedException

def get_all_users(*, session: Session, skip: int = 0, limit: int = 10) -> List[User]:
    statement = select(User).offset(skip).limit(limit)
    users = session.exec(statement).all()
    return users


def create_user(*, session: Session, user_create: UserCreate) -> UserResponse:
    db_obj = User.model_validate(
        user_create, update={
            "hashed_password": get_password_hash(user_create.password)
        }
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj

def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def delete_user(*, session: Session, user_id: int) -> Any:
    db_user = session.get(User, user_id)
    if not db_user:
        raise UserNotFoundException()
    session.delete(db_user)
    session.commit()
    return db_user

def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user

def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        raise InvalidCredentialsException()
    if db_user.is_locked:
        raise UserLockedException()
    if not verify_password(password, db_user.hashed_password):
        db_user.login_attempts += 1
        if db_user.login_attempts >= 5:
            db_user.is_locked = True
        session.commit()
        raise InvalidCredentialsException()
    db_user.login_attempts = 0
    session.commit()
    return db_user