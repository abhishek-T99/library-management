# Library Managemet API

## Setting up the Project for Development

### Prerequisites

Ensure you have the following installed on your system or hosted on docker:

1. **Python**
2. **RabbitMQ**
3. **Redis**

### Installation Steps

1. **Clone the repository**:

```bash
git clone https://github.com/abhishek-T55/library-management.git
cd library-management
```

2. **Install Python dependencies**:

```bash
pip install -r requirements.txt
```

3. **Create and configure the `.env` file.**:

   Create a `.env` file in the project root directory. A sample file `.env.example` is provided. Copy its content to `.env` and update the configuration variables accordingly.

```bash
cp .env.sample .env
```

4. **Run the database migration**:

```bash
alembic upgrade heads
```

5. **Start RabbitMQ**:

   If RabbitMQ is not already running, start it with:

```bash
rabbitmq-server
```

6. **Start Redis**:

   If Redis is not already running, start it with:

```bash
redis-server
```

7. **Run the Celery worker**:

   Start the celery worker to handle background tasks:

```bash
celery -A app.services.task_scheduler.celery_app worker --loglevel=info
```

8. **Run the FastAPI Project**:

   Start the FastAPI server with:

```bash
uvicorn app.main:app --reload
```
