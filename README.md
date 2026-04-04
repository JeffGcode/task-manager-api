# Task Manager API

A REST API for managing tasks with user authentication.

## Features

- User registration and JWT authentication
- Create, read, update, delete tasks
- Categorize tasks
- Full test suite
- Dockerized
- CI/CD with GitHub Actions

## Live Demo

[Deployed on Railway](#) – (add URL after deployment)

## Local Development

1. Clone the repository
2. Create a virtual environment and install dependencies:

task-manager-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── auth.py
│   ├── crud.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── users.py
│   │   ├── tasks.py
│   │   └── categories.py
│   └── dependencies.py
├── tests/
│   ├── __init__.py
│   ├── test_users.py
│   ├── test_tasks.py
│   └── conftest.py
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .github/workflows/ci.yml
└── README.md