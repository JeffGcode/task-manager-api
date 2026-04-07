import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, get_db
from app.config import settings
import os

# Use the test database URL from environment, or default
# In GitHub Actions, we set DATABASE_URL to point to the PostgreSQL service.
# For local testing, we can use a separate test database.
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/taskdb_test")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    # Create tables before any tests run
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables after all tests finish (optional, but good for cleanup)
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Provide a transactional session for tests that need direct DB access."""
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client