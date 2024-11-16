from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.core.auth import get_current_user
from app.schemas.profile import ProfileCreate, ProfileUpdate, ProfileResponse
from app.services.profile_service import ProfileService

router = APIRouter()

@router.post("/", response_model=ProfileResponse)
async def create_profile(
    profile: ProfileCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create new profile for authenticated user."""
    service = ProfileService(db)
    return await service.create_profile(profile)

@router.get("/me", response_model=ProfileResponse)
async def get_my_profile(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Get current user's profile."""
    service = ProfileService(db)
    profile = await service.get_profile_by_auth_id(current_user["id"])
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.patch("/me", response_model=ProfileResponse)
async def update_my_profile(
    update_data: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update current user's profile."""
    service = ProfileService(db)
    return await service.update_profile(current_user["id"], update_data)