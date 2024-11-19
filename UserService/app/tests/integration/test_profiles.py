import pytest
from fastapi import status

class TestProfiles:
    def test_create_profile_success(self, client):
        """Test successful profile creation."""
        response = client.post(
            "/api/v1/profiles/",
            json={
                "auth_user_id": 1,
                "email": "test@example.com"
            }
        )
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["email"] == "test@example.com"
        assert response.json()["auth_user_id"] == 1

    def test_create_duplicate_profile(self, client):
        """Test creating duplicate profile."""
        # Create first profile
        client.post(
            "/api/v1/profiles/",
            json={
                "auth_user_id": 1,
                "email": "test@example.com"
            }
        )
        
        # Try to create duplicate profile
        response = client.post(
            "/api/v1/profiles/",
            json={
                "auth_user_id": 1,
                "email": "test@example.com"
            }
        )
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Profile already exists" in response.json()["detail"]

    def test_get_my_profile(self, client, auth_headers):
        """Test getting user's own profile."""
        response = client.get(
            "/api/v1/profiles/me",
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert "email" in response.json()
        assert "auth_user_id" in response.json()

    def test_get_profiles_list(self, client, auth_headers):
        """Test getting list of profiles."""
        response = client.get(
            "/api/v1/profiles/",
            headers=auth_headers
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.json(), list)