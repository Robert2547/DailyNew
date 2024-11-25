import pytest
from app.core.config import settings
from app.models.user import User, TokenInfo
from app.core.security import get_password_hash
import logging

logger = logging.getLogger(__name__)

@pytest.fixture(autouse=True)
def clear_tables(db_session):
    """Clear tables before each test."""
    # Clear tables in correct order due to foreign key constraints
    db_session.query(TokenInfo).delete()
    db_session.query(User).delete()
    db_session.commit()

@pytest.fixture
def test_credentials():
    """Return test user credentials."""
    return {
        "email": "test@example.com",
        "password": "TestPassword123!"
    }

@pytest.fixture
def test_db_user(db_session, test_credentials):
    """Create and return a test user."""
    user = User(
        email=test_credentials["email"],
        hashed_password=get_password_hash(test_credentials["password"]),
        is_active=True
    )
    db_session.add(user)
    db_session.commit()
    
    # Get fresh instance
    db_user = db_session.query(User).filter(User.email == test_credentials["email"]).first()
    return db_user

def test_login_success(client, db_session, test_credentials, test_db_user):
    """Test successful login."""
    login_data = {
        "username": test_credentials["email"],
        "password": test_credentials["password"]
    }

    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Verify token in database
    db_token = db_session.query(TokenInfo)\
        .join(User, User.id == TokenInfo.user_id)\
        .filter(User.email == test_credentials["email"])\
        .first()
    
    assert db_token is not None
    assert db_token.access_token == data["access_token"]

def test_login_wrong_password(client, test_credentials, test_db_user):
    """Test login with wrong password."""
    login_data = {
        "username": test_credentials["email"],
        "password": "WrongPassword123!"
    }

    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

def test_login_nonexistent_user(client):
    """Test login with non-existent user."""
    login_data = {
        "username": "nonexistent@example.com",
        "password": "TestPassword123!"
    }

    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"

def test_verify_token(client, db_session, test_credentials, test_db_user):
    """Test token verification after login."""
    # First, let's debug the login process
    login_data = {
        "username": test_credentials["email"],
        "password": test_credentials["password"]
    }

    print("\nDebug login process:")
    print(f"Login data: {login_data}")
    
    # Get token
    login_response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data=login_data,
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )

    print(f"Login response status: {login_response.status_code}")
    print(f"Login response body: {login_response.json()}")

    # Verify login was successful
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    print("\nDebug token verification:")
    print(f"Token: {token}")
    
    # Test token verification
    verify_response = client.post(
        f"{settings.API_V1_STR}/auth/verify-token",
        headers={"Authorization": f"Bearer {token}"}
    )

    print(f"Verify response status: {verify_response.status_code}")
    print(f"Verify response body: {verify_response.json()}")

    # For debugging, let's check the actual user in the database
    current_user = db_session.query(User).filter(
        User.email == test_credentials["email"]
    ).first()
    print(f"\nCurrent user in DB:")
    print(f"ID: {current_user.id}")
    print(f"Email: {current_user.email}")
    print(f"Is active: {current_user.is_active}")

    assert verify_response.status_code == 200

def test_verify_invalid_token(client):
    """Test verification with invalid token."""
    response = client.post(
        f"{settings.API_V1_STR}/auth/verify-token",
        headers={"Authorization": "Bearer invalid_token"}
    )

    assert response.status_code == 401
    assert "Could not validate credentials" in response.json()["detail"]

def test_verify_missing_token(client):
    """Test verification without token."""
    response = client.post(f"{settings.API_V1_STR}/auth/verify-token")

    assert response.status_code == 401
    assert response.json()["detail"] == "Not authenticated"