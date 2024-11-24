import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from fastapi.testclient import TestClient
from main import app
from app.db.base import Base
from app.api.deps import get_db

@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    """Setup test environment variables."""
    os.environ.update({
        "TESTING": "true",
        "DB_USER": "test_user",
        "DB_PASSWORD": "test_password",
        "POSTGRES_HOST": "localhost",
        "USER_DB_NAME": "user_test_db",
        "USER_DB_PORT": "5437",
        "AUTH_SERVICE_URL": "http://auth_service:8001"
    })

@pytest.fixture(scope="session")
def test_db(setup_test_env):
    """Create test database connection."""
    # Use a direct database URL for testing
    database_url = "postgresql://test_user:test_password@localhost:5437/user_test_db"
    engine = create_engine(database_url)
    
    # Create all tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    yield engine
    
    # Cleanup
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(test_db):
    """Create database session for testing."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_db)
    
    with TestingSessionLocal() as session:
        yield session

@pytest.fixture(scope="function")
def client(db_session):
    """Create test client with DB session."""
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()