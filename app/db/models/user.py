from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr
from typing import List


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=200)
    is_locked: bool = False
    full_name: str | None = Field(default=None, max_length=100)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=20)


class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=200)
    password: str | None = Field(default=None, min_length=8, max_length=20)


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    login_attempts: int = Field(default=0)
    books: List["Book"] = Relationship(back_populates="owner")


class UserPublic(SQLModel):
    id: int


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(SQLModel):
    sub: int | None = None