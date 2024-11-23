import pytest
from app.core.config import settings

def test_signup_success(client, mock_user_service):
    """Test successful user signup."""
    # Test data with valid password format
    user_data = {
        "email": "test@example.com",
        "password": "TestPassword123!",  # Added special character !
        "password_confirm": "TestPassword123!"
    }

    # Print for debugging
    print(f"\nMaking request to: {settings.API_V1_STR}/auth/signup")
    print(f"With data: {user_data}")

    # Make request
    response = client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json=user_data
    )

    # Print response for debugging
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.json()}")

    # Assertions
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert "id" in data

def test_signup_password_mismatch(client):
    """Test signup with mismatched passwords."""
    user_data = {
        "email": "test@example.com",
        "password": "TestPassword123!",
        "password_confirm": "DifferentPassword123!"
    }

    response = client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json=user_data
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Passwords do not match"

def test_signup_password_no_uppercase(client):
    """Test signup with password missing uppercase letter."""
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123!",
        "password_confirm": "testpassword123!"
    }

    response = client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json=user_data
    )

    assert response.status_code == 422
    assert "Password must contain at least one uppercase letter" in response.json()["detail"][0]["msg"]

def test_signup_password_no_special_char(client):
    """Test signup with password missing special character."""
    user_data = {
        "email": "test@example.com",
        "password": "TestPassword123",
        "password_confirm": "TestPassword123"
    }

    response = client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json=user_data
    )

    assert response.status_code == 422
    assert "Password must contain at least one special character" in response.json()["detail"][0]["msg"]

def test_signup_duplicate_email(client, mock_user_service):
    """Test signup with duplicate email."""
    user_data = {
        "email": "test@example.com",
        "password": "TestPassword123!",
        "password_confirm": "TestPassword123!"
    }

    # Create first user
    client.post(f"{settings.API_V1_STR}/auth/signup", json=user_data)

    # Try to create duplicate user
    response = client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json=user_data
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "The user with this email already exists"

def test_signup_invalid_email_format(client):
    """Test signup with invalid email format."""
    user_data = {
        "email": "invalid-email",
        "password": "TestPassword123!",
        "password_confirm": "TestPassword123!"
    }

    response = client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json=user_data
    )

    assert response.status_code == 422
    assert "value is not a valid email address" in response.json()["detail"][0]["msg"]