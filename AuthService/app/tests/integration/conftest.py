# app/tests/integration/conftest.py

import pytest
import sys
import os
from pathlib import Path

# Set testing environment variable before imports
os.environ["TESTING"] = "1"

# Add the root directory to Python path
root_dir = Path(__file__).parent.parent.parent.parent
sys.path.append(str(root_dir))

from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from app.core.test_config import test_settings
from app.db.base import Base, get_engine, init_db
from main import app
from app.api import deps
import logging

logger = logging.getLogger(__name__)

def verify_db_connection(database_url: str, retries: int = 5) -> bool:
    """Verify database connection with retries."""
    import time
    from sqlalchemy import create_engine
    from sqlalchemy.exc import OperationalError

    for attempt in range(retries):
        try:
            engine = create_engine(database_url)
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            engine.dispose()
            return True
        except OperationalError as e:
            logger.warning(f"Database connection attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(2)
            continue
    return False

def pytest_configure(config):
    """Verify database connection before running any tests."""
    logger.info("Verifying database connection before running tests...")
    
    database_url = "postgresql://test_user:test_password@localhost:5436/auth_test_db"
    
    if not verify_db_connection(database_url):
        logger.error("Database is not accessible! Stopping tests.")
        pytest.exit("Database connection failed")

@pytest.fixture(scope="session")
def db_engine():
    """Create database engine for testing."""
    # Initialize the database
    init_db()
    from app.db.base import engine
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(db_engine):
    """Create database session for each test."""
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=db_engine
    )
    
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function")
def client(db_session):
    """Create FastAPI test client with database override."""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    # Override get_db
    app.dependency_overrides[deps.get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture(scope="function")
def test_user(client):
    """Create test user and return user data."""
    user_data = {
        "email": test_settings.TEST_USER_EMAIL,
        "password": test_settings.TEST_USER_PASSWORD,
        "password_confirm": test_settings.TEST_USER_PASSWORD
    }
    response = client.post(f"{test_settings.API_V1_STR}/auth/signup", json=user_data)
    return response.json()

@pytest.fixture(scope="function")
def auth_headers(client, test_user):
    """Get authentication headers for test user."""
    response = client.post(
        f"{test_settings.API_V1_STR}/auth/login",
        data={
            "username": test_settings.TEST_USER_EMAIL,
            "password": test_settings.TEST_USER_PASSWORD
        }
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

# Optional: Add cleanup fixture
@pytest.fixture(autouse=True)
def cleanup_database(db_session):
    """Clean up database after each test."""
    yield
    for table in reversed(Base.metadata.sorted_tables):
        db_session.execute(table.delete())
    db_session.commit()