# Signit - Simple FastAPI Application

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)

Signit is a simple FastAPI application that utilizes Beanie as an ODM for MongoDB. It provides a scalable and efficient way to manage APIs with integrated authentication and background task processing.

## Table of Contents

- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Setup and Usage](#setup-and-usage)
- [Environment Configuration](#environment-configuration)
- [Running the Application](#running-the-application)
- [Running Celery Worker](#running-celery-worker)
- [Running test cases](#running-test-cases)
- [Docker Usage](#docker-usage)
- [API Documentation](#api-documentation)

## Getting Started

These instructions will help you set up the project for development and testing purposes.

## Prerequisites

- **Python 3.10+**: Ensure Python is installed and accessible in your system PATH.
- **Git**: For cloning the repository.
- **Redis 5+**: Required as a Celery broker for managing background tasks.
- **[Poetry](https://python-poetry.org/)**: For managing Python dependencies.
- **[MongoDB](https://www.mongodb.com/docs/manual/introduction/)**: Used as the main database for the application.

### Installing Redis and MongoDB

- **Redis**: Follow the [official installation guide](https://redis.io/download) to install Redis.
- **MongoDB**: Follow the [official installation guide](https://www.mongodb.com/docs/manual/installation/) to install MongoDB.

## Setup and Usage

1. **Clone the repository**:

    ```bash
       git clone https://github.com/abdalkreemorabi/signit-task
    ```

2. **Navigate to the project root directory**:

    ```bash
    cd signit-task
    ```

### Environment Configuration

3. **Create a `.env` file** in the project root with the following content:

    ```bash
    touch .env
    vim .env
    ```

    ```env
    MONGO_DB_HOST="localhost"
    MONGO_DB_PORT=27017
    MONGO_DB_USERNAME="admin"
    MONGO_DB_PASSWORD="admin"
    MONGO_DB_DATABASE="signit"
    SECRET_KEY="secret"
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES="1030"
    CELERY_BROKER_URL="redis://localhost:6379/0"
    SENTRY_DSN=""
    ```

4. **Activate Poetry**:

    ```bash
    poetry shell
    ```

5. **Install the dependencies**:

    ```bash
    poetry install
    ```

## Running the Application

To start the FastAPI application, run:

```bash
uvicorn app.main:app --reload --port 8000
```
## Running Celery Worker

To start Celery worker, run:

```bash
celery -A app.celery.app worker --loglevel=INFO
```

## Running test cases

To run the tests, type:

```bash
pytest -xv
```

## Docker Usage

<h5>There are also [Dockerfile](Dockerfile)
to run the service and [Dockerfile-worker](Dockerfile-worker) to run the worker
for easy deployment.</h5>

---
### API documentation

All APIs are available on `{{base_url}}/docs` or
`{{base_url}}/redoc` paths with Swagger or ReDoc.
