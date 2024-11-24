import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.db.base import Base, init_db
from app.api.deps import get_db
import os
from fastapi.testclient import TestClient
import httpx
from main import app
import asyncio

@pytest.fixture(scope="session", autouse=True)
def setup_test_env():
    """Setup test environment variables."""
    os.environ.update({
        "TESTING": "true",
        "DB_USER": "test_user",
        "DB_PASSWORD": "test_password",
        "AUTH_DB_NAME": "auth_test_db",
        "AUTH_DB_PORT": "5436",
        "POSTGRES_HOST": "localhost",
        "USER_SERVICE_URL": "http://user_service:8002",
        "SECRET_KEY": "test-secret-key-123",  
        "ALGORITHM": "HS256"
    })
    
    # Reinitialize database with test settings
    init_db()

@pytest.fixture(scope="session")
def test_db(setup_test_env):
    """Create test database URL."""
    from app.core.config import settings
    database_url = settings.get_database_url
    
    # Create engine and tables
    engine = create_engine(database_url)
    
    # Drop and recreate all tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    yield database_url
    
    # Cleanup
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session(test_db):
    """Create database session for testing."""
    engine = create_engine(test_db)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
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

@pytest.fixture
def mock_user_service():
    """Mock UserService responses."""
    async def mock_response(*args, **kwargs):
        return httpx.Response(
            status_code=201,
            json={
                "id": 1,
                "email": "test@example.com",
                "auth_user_id": 1
            }
        )
    
    with pytest.MonkeyPatch.context() as m:
        m.setattr(httpx.AsyncClient, "post", mock_response)
        yield