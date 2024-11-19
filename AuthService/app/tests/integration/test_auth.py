
import pytest
from fastapi import status
import httpx
from unittest.mock import patch, AsyncMock
from app.core.test_config import test_settings

class TestAuthSignup:
    async def test_signup_success(self, client):
        """Test successful user signup."""
        test_email = "new@example.com"
        mock_profile_response = httpx.Response(201, json={"id": 1, "email": test_email})
        
        # Mock the httpx.AsyncClient.post call
        with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
            mock_post.return_value = mock_profile_response
            
            response = client.post(
                f"{test_settings.API_V1_STR}/auth/signup",
                json={
                    "email": test_email,
                    "password": test_settings.TEST_USER_PASSWORD,
                    "password_confirm": test_settings.TEST_USER_PASSWORD
                }
            )
            
            assert response.status_code == status.HTTP_201_CREATED
            assert response.json()["email"] == test_email
            assert "id" in response.json()

            # Verify the mock was called with correct arguments
            mock_post.assert_called_once_with(
                f"{test_settings.USER_SERVICE_URL}/api/v1/profiles/",
                json={
                    "auth_user_id": response.json()["id"],
                    "email": test_email
                }
            )

    async def test_signup_password_mismatch(self, client):
        """Test signup with mismatched passwords."""
        response = client.post(
            f"{test_settings.API_V1_STR}/auth/signup",
            json={
                "email": "test@example.com",
                "password": test_settings.TEST_USER_PASSWORD,
                "password_confirm": "different_password"
            }
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Passwords do not match" in response.json()["detail"]

    async def test_signup_existing_email(self, client, test_user):
        """Test signup with existing email."""
        response = client.post(
            f"{test_settings.API_V1_STR}/auth/signup",
            json={
                "email": test_settings.TEST_USER_EMAIL,
                "password": test_settings.TEST_USER_PASSWORD,
                "password_confirm": test_settings.TEST_USER_PASSWORD
            }
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "already exists" in response.json()["detail"]

class TestAuthLogin:
    async def test_login_success(self, client, test_user):
        """Test successful login."""
        response = client.post(
            f"{test_settings.API_V1_STR}/auth/login",
            data={
                "username": test_settings.TEST_USER_EMAIL,
                "password": test_settings.TEST_USER_PASSWORD
            }
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"

    async def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials."""
        response = client.post(
            f"{test_settings.API_V1_STR}/auth/login",
            data={
                "username": "wrong@example.com",
                "password": "wrongpassword"
            }
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert "Incorrect email or password" in response.json()["detail"]

class TestTokenVerification:
    async def test_verify_token_success(self, client, auth_headers):
        """Test successful token verification."""
        response = client.post(
            f"{test_settings.API_V1_STR}/auth/verify-token",
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert "email" in response.json()
        assert "id" in response.json()

    async def test_verify_token_invalid(self, client):
        """Test invalid token verification."""
        response = client.post(
            f"{test_settings.API_V1_STR}/auth/verify-token",
            headers={"Authorization": "Bearer invalid_token"}
        )
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED