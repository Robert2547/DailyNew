import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
import os

@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    """Setup test environment variables."""
    os.environ["TESTING"] = "true"
    os.environ["DB_USER"] = "test_user"
    os.environ["DB_PASSWORD"] = "test_password"
    os.environ["AUTH_DB_NAME"] = "auth_test_db"
    os.environ["AUTH_DB_PORT"] = "5436"
    os.environ["POSTGRES_HOST"] = "localhost"

@pytest.fixture(scope="session")
def test_db(setup_test_env):
    """Create test database URL."""
    database_url = (
        f"postgresql://{os.getenv('DB_USER')}:"
        f"{os.getenv('DB_PASSWORD')}@"
        f"{os.getenv('POSTGRES_HOST')}:"
        f"{os.getenv('AUTH_DB_PORT')}/"
        f"{os.getenv('AUTH_DB_NAME')}"
    )
    return database_url

@pytest.fixture(scope="session")
def db_engine(test_db):
    """Create test database engine."""
    engine = create_engine(test_db)
    yield engine
    engine.dispose()