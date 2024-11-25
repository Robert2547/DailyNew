# app/tests/integration/test_profiles.py

import pytest
from fastapi import status
from app.schemas.profile import ProfileCreate
from unittest.mock import patch
from app.core.auth import get_current_user

pytestmark = pytest.mark.asyncio


@pytest.fixture
def mock_current_user():
    return {"id": 1, "email": "test@example.com"}


@pytest.fixture
def profile_data():
    return {
        "auth_user_id": 1,
        "full_name": "Test User",
        "bio": "Test bio",
        "avatar_url": "http://example.com/avatar.jpg",
    }


@pytest.fixture
def auth_headers():
    return {"Authorization": "Bearer test-token"}


@pytest.mark.asyncio
async def test_create_profile(client, db_session, profile_data):
    """Test creating a new profile."""
    response = client.post("/api/v1/profiles/", json=profile_data)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["auth_user_id"] == profile_data["auth_user_id"]
    assert data["full_name"] == profile_data["full_name"]


@pytest.mark.asyncio
async def test_create_duplicate_profile(client, db_session, profile_data):
    """Test creating a duplicate profile."""
    # Create first profile
    client.post("/api/v1/profiles/", json=profile_data)
    # Try to create duplicate
    response = client.post("/api/v1/profiles/", json=profile_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_get_my_profile(
    client, db_session, profile_data, auth_headers, mock_current_user
):
    """Test getting current user's profile."""
    # Override the dependency
    app = client.app
    app.dependency_overrides[get_current_user] = lambda: mock_current_user

    # First create a profile
    client.post("/api/v1/profiles/", json=profile_data)

    # Then get my profile
    response = client.get("/api/v1/profiles/me", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["auth_user_id"] == profile_data["auth_user_id"]

    # Clean up
    app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_get_profiles_pagination(
    client, db_session, auth_headers, mock_current_user
):
    """Test profiles pagination."""
    # Override the dependency
    app = client.app
    app.dependency_overrides[get_current_user] = lambda: mock_current_user

    # Create multiple profiles
    profiles = [
        {"auth_user_id": i, "full_name": f"User {i}", "bio": f"Bio {i}"}
        for i in range(1, 4)
    ]

    for profile in profiles:
        client.post("/api/v1/profiles/", json=profile)

    # Test pagination
    response = client.get("/api/v1/profiles/?skip=0&limit=2", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2

    # Clean up
    app.dependency_overrides.clear()
