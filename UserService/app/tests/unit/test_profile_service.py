# app/tests/unit/test_profile_service.py

import pytest
from app.services.profile_service import ProfileService
from app.schemas.profile import ProfileCreate, ProfileUpdate
from app.models.profile import UserProfile


@pytest.fixture
def profile_service(db_session):
    return ProfileService(db_session)


@pytest.fixture
def profile_data():
    return {
        "auth_user_id": 1,
        "full_name": "Test User",
        "bio": "Test bio",
        "avatar_url": "http://example.com/avatar.jpg",
    }


@pytest.fixture(autouse=True)
def cleanup_profiles(db_session):
    """Cleanup all profiles before and after each test."""
    # Clean before test
    db_session.query(UserProfile).delete()
    db_session.commit()

    yield

    # Clean after test
    db_session.query(UserProfile).delete()
    db_session.commit()


@pytest.mark.asyncio
async def test_create_profile(profile_service, profile_data):
    """Test profile creation through service."""
    profile = await profile_service.create_profile(ProfileCreate(**profile_data))
    assert profile.auth_user_id == profile_data["auth_user_id"]
    assert profile.full_name == profile_data["full_name"]


@pytest.mark.asyncio
async def test_create_duplicate_profile(profile_service, profile_data):
    """Test creating a duplicate profile raises error."""
    # Create first profile
    await profile_service.create_profile(ProfileCreate(**profile_data))

    # Try to create duplicate
    with pytest.raises(Exception) as exc_info:
        await profile_service.create_profile(ProfileCreate(**profile_data))
    assert "unique constraint" in str(exc_info.value).lower()


@pytest.mark.asyncio
async def test_get_profile_by_auth_id(profile_service):
    """Test getting profile by auth ID."""
    # Create profile with unique auth_user_id
    profile_data = {
        "auth_user_id": 2,  # Different ID
        "full_name": "Test User 2",
        "bio": "Test bio",
        "avatar_url": "http://example.com/avatar.jpg",
    }
    created_profile = await profile_service.create_profile(
        ProfileCreate(**profile_data)
    )

    # Retrieve it
    profile = await profile_service.get_profile_by_auth_id(profile_data["auth_user_id"])
    assert profile is not None
    assert profile.id == created_profile.id
    assert profile.auth_user_id == profile_data["auth_user_id"]


@pytest.mark.asyncio
async def test_update_profile(profile_service):
    """Test profile update."""
    # Create profile with unique auth_user_id
    initial_data = {
        "auth_user_id": 3,  # Different ID
        "full_name": "Test User 3",
        "bio": "Original bio",
        "avatar_url": "http://example.com/avatar.jpg",
    }
    profile = await profile_service.create_profile(ProfileCreate(**initial_data))

    # Update profile
    update_data = {"full_name": "Updated Name", "bio": "Updated bio"}
    updated_profile = await profile_service.update_profile(
        profile.auth_user_id, ProfileUpdate(**update_data)
    )

    assert updated_profile.full_name == update_data["full_name"]
    assert updated_profile.auth_user_id == initial_data["auth_user_id"]


@pytest.mark.asyncio
async def test_get_nonexistent_profile(profile_service):
    """Test getting a profile that doesn't exist."""
    profile = await profile_service.get_profile_by_auth_id(999)
    assert profile is None


@pytest.mark.asyncio
async def test_update_nonexistent_profile(profile_service):
    """Test updating a profile that doesn't exist."""
    update_data = {"full_name": "Updated Name"}
    updated_profile = await profile_service.update_profile(
        999, ProfileUpdate(**update_data)
    )
    assert updated_profile is None
