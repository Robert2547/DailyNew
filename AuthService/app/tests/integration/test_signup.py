import pytest
from app.core.config import settings
import httpx


def test_signup_success(client, mock_user_service):
    """Test successful user signup."""
    user_data = {
        "email": "test@example.com",
        "password": "TestPassword123!",
        "password_confirm": "TestPassword123!"
    }

    response = client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json=user_data
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert "id" in data

def test_signup_validation_errors(client):
    """Test various password validation scenarios."""
    test_cases = [
        {
            "case": "password_mismatch",
            "data": {
                "email": "test@example.com",
                "password": "TestPassword123",
                "password_confirm": "DifferentPassword123"
            },
            "expected_msg": "passwords do not match"
        },
        {
            "case": "missing_uppercase",
            "data": {
                "email": "test@example.com",
                "password": "testpassword123",
                "password_confirm": "testpassword123"
            },
            "expected_msg": "Password must contain at least one uppercase letter"
        },
        {
            "case": "too_short",
            "data": {
                "email": "test@example.com",
                "password": "Test1",
                "password_confirm": "Test1"
            },
            "expected_msg": "string should have at least 8 characters"
        }
    ]

    for test_case in test_cases:
        response = client.post(
            f"{settings.API_V1_STR}/auth/signup",
            json=test_case["data"]
        )
        
        assert response.status_code == 422, f"Expected 422 status code for {test_case['case']}, got {response.status_code} with response: {response.json()}"
        
        error_detail = response.json()["detail"]
        error_messages = [error["msg"].lower() for error in error_detail]
        
        assert any(
            test_case["expected_msg"].lower() in error_msg
            for error_msg in error_messages
        ), f"Expected '{test_case['expected_msg']}' in error messages for {test_case['case']}. Got: {error_messages}"

def test_signup_duplicate_email(client, mock_user_service):
    """Test signup with duplicate email."""
    user_data = {
        "email": "test@example.com",
        "password": "TestPassword123!",
        "password_confirm": "TestPassword123!"
    }

    # Create first user
    response = client.post(f"{settings.API_V1_STR}/auth/signup", json=user_data)
    assert response.status_code == 400

    # Try to create duplicate user
    response = client.post(
        f"{settings.API_V1_STR}/auth/signup",
        json=user_data
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "The user with this email already exists"

def test_signup_invalid_email(client):
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