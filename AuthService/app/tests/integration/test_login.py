import pytest
from app.core.config import settings
from app.models.user import User, TokenInfo
from app.core.security import get_password_hash
import logging

logger = logging.getLogger(__name__)

@pytest.fixture(scope="function")
def test_credentials():
    """Return test user credentials instead of User object."""
    return {
        "email": "test@example.com",
        "password": "TestPassword123!"
    }

@pytest.fixture(scope="function")
def test_db_user(db_session, test_credentials):
    """Create test user in database."""
    user = User(
        email=test_credentials["email"],
        hashed_password=get_password_hash(test_credentials["password"]),
        is_active=True
    )
    db_session.add(user)
    db_session.commit()

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

    # Basic assertions for response
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # Verify token in database with a new query
    db_token = db_session.query(TokenInfo)\
        .join(User, User.id == TokenInfo.user_id)\
        .filter(User.email == test_credentials["email"])\
        .first()
    
    assert db_token is not None, "Token not found in database"
    assert db_token.access_token == data["access_token"]

# def test_login_wrong_password(client, test_user):
#     """Test login with wrong password."""
#     login_data = {
#         "username": "test@example.com",
#         "password": "WrongPassword123!"
#     }

#     response = client.post(
#         f"{settings.API_V1_STR}/auth/login",
#         data=login_data,
#         headers={"Content-Type": "application/x-www-form-urlencoded"}
#     )

#     assert response.status_code == 401
#     assert response.json()["detail"] == "Incorrect email or password"

# def test_login_nonexistent_user(client):
#     """Test login with non-existent user."""
#     login_data = {
#         "username": "nonexistent@example.com",
#         "password": "TestPassword123!"
#     }

#     response = client.post(
#         f"{settings.API_V1_STR}/auth/login",
#         data=login_data,
#         headers={"Content-Type": "application/x-www-form-urlencoded"}
#     )

#     assert response.status_code == 401
#     assert response.json()["detail"] == "Incorrect email or password"

# def test_login_inactive_user(client, test_user, db_session):
#     """Test login with inactive user."""
#     # Deactivate user
#     test_user.is_active = False
#     db_session.commit()

#     login_data = {
#         "username": "test@example.com",
#         "password": "TestPassword123!"
#     }

#     response = client.post(
#         f"{settings.API_V1_STR}/auth/login",
#         data=login_data,
#         headers={"Content-Type": "application/x-www-form-urlencoded"}
#     )

#     assert response.status_code == 401
#     assert response.json()["detail"] == "Incorrect email or password"

# def test_verify_token(client, db_session, test_credentials, test_db_user):
#     """Test token verification after login."""
#     # First get the user from database for comparison
#     user = db_session.query(User).filter(
#         User.email == test_credentials["email"]
#     ).first()
#     assert user is not None, "Test user not found in database"

#     # Login to get token
#     login_data = {
#         "username": test_credentials["email"],
#         "password": test_credentials["password"]
#     }

#     login_response = client.post(
#         f"{settings.API_V1_STR}/auth/login",
#         data=login_data,
#         headers={"Content-Type": "application/x-www-form-urlencoded"}
#     )

#     assert login_response.status_code == 200
#     token = login_response.json()["access_token"]

#     # Test token verification
#     verify_response = client.post(
#         f"{settings.API_V1_STR}/auth/verify-token",
#         headers={"Authorization": f"Bearer {token}"}
#     )

#     print(f"\nVerify response status: {verify_response.status_code}")
#     print(f"Verify response body: {verify_response.json()}")

#     assert verify_response.status_code == 200
#     user_data = verify_response.json()

#     # Compare with fresh user data from database
#     assert user_data["email"] == user.email
#     assert user_data["id"] == user.id
#     assert user_data["is_active"] == user.is_active

# def test_verify_invalid_token(client):
#     """Test verification with invalid token."""
#     response = client.post(
#         f"{settings.API_V1_STR}/auth/verify-token",
#         headers={"Authorization": "Bearer invalid_token"}
#     )

#     assert response.status_code == 401
#     assert "Could not validate credentials" in response.json()["detail"]

# def test_verify_missing_token(client):
#     """Test verification without token."""
#     response = client.post(f"{settings.API_V1_STR}/auth/verify-token")

#     assert response.status_code == 401
#     assert response.json()["detail"] == "Not authenticated"
