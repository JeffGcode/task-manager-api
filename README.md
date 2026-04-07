markdown
# Task Manager API

A production‑ready REST API for managing tasks, built with **FastAPI**, **PostgreSQL**, **JWT authentication**, **Docker**, and **CI/CD**.  
Deployed on Railway – test it live below.

## 🚀 Live URL
[https://task-manager-api.up.railway.app](https://task-manager-api.up.railway.app)  
*(Replace with your actual Railway URL)*

Interactive API documentation (Swagger UI) is available at `/docs`.

## ✨ Features
- User registration & login (JWT tokens)
- Create, read, update, delete tasks
- Organise tasks into categories
- Password hashing (pbkdf2_sha256)
- PostgreSQL database with SQLAlchemy ORM
- Alembic migrations
- Pytest unit & integration tests
- Docker & docker‑compose for local development
- GitHub Actions CI (tests on every push)
- Automatic deployment to Railway on `main` branch

## 🛠️ Tech Stack
- **FastAPI** – modern Python web framework
- **PostgreSQL** – relational database
- **SQLAlchemy** – ORM
- **Alembic** – database migrations
- **python-jose** – JWT handling
- **passlib** – password hashing
- **Pytest** – testing
- **Docker** – containerisation
- **Railway** – cloud deployment

## 🧪 Test the API Live
You can use the Swagger UI at `{live_url}/docs` or send requests with `curl`.

### Example requests (using the live URL)
```bash
# Register a user
curl -X POST "https://task-manager-api.up.railway.app/users/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"secret123"}'

# Login to get a token
curl -X POST "https://task-manager-api.up.railway.app/users/token" \
  -d "grant_type=password&username=testuser&password=secret123"

# Create a category (replace <token>)
curl -X POST "https://task-manager-api.up.railway.app/categories/" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"name":"Work"}'

# Create a task
curl -X POST "https://task-manager-api.up.railway.app/tasks/" \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"title":"Finish README","category_id":1}'
🐳 Run Locally with Docker
bash
git clone https://github.com/JeffGcode/task-manager-api.git
cd task-manager-api
docker-compose up --build
The API will be available at http://localhost:8000.

🧪 Run Tests
bash
# Create a virtual environment and install dependencies
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\activate on Windows
pip install -r requirements.txt

# Run tests with coverage
pytest -v --cov=app
📁 Project Structure
text
task-manager-api/
├── app/
│   ├── routers/         # API endpoints
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   ├── crud.py          # database operations
│   ├── auth.py          # JWT & password handling
│   ├── database.py      # DB connection
│   └── main.py          # FastAPI app
├── tests/               # pytest suite
├── alembic/             # migrations
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── .github/workflows/ci.yml   # CI/CD pipeline
📄 License
MIT

👤 Author
Jeffrey Gonzalez – GitHub

text

---

## 2. Implement CI/CD: GitHub Actions to Test & Deploy to Railway

We already have a CI workflow that runs tests on every push (`ci.yml`). Now we add **automatic deployment to Railway** when pushing to `main`. Railway provides a GitHub Action for this.

### Steps

#### 2.1 Get a Railway API token
- Log in to [Railway.app](https://railway.app).
- Go to **Settings** → **API Tokens** → **Create a new token**.
- Give it a name (e.g., `github-actions`), copy the token (it starts with `rail_...`).

#### 2.2 Add the token as a GitHub secret
- Go to your GitHub repository → **Settings** → **Secrets and variables** → **Actions**.
- Click **New repository secret**.
- Name: `RAILWAY_TOKEN`
- Value: paste the token you copied.

#### 2.3 Update your `.github/workflows/ci.yml`

We will extend the existing file to:
- Run tests on every push (already there).
- On push to `main`, also deploy to Railway using the official Railway action.

**Updated `.github/workflows/ci.yml`** (replace the entire content):

```yaml
name: CI/CD

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_USER: user
          POSTGRES_PASSWORD: password
          POSTGRES_DB: taskdb_test
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run tests
        env:
          DATABASE_URL: postgresql://user:password@localhost/taskdb_test
          SECRET_KEY: testsecret
          ALGORITHM: HS256
          ACCESS_TOKEN_EXPIRE_MINUTES: 30
        run: |
          pytest -v --cov=app

  deploy:
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4
      - name: Deploy to Railway
        uses: railwayhq/railway-action@v3
        with:
          token: ${{ secrets.RAILWAY_TOKEN }}