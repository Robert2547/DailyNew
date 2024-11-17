from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.api import deps
from app.models.profile import UserProfile
from app.schemas.profile import ProfileCreate, ProfileResponse
from typing import List
import logging
from app.core.auth import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(
    profile_in: ProfileCreate,
    db: Session = Depends(deps.get_db)
) -> ProfileResponse:
    """Create new user profile."""
    # Check if profile already exists
    if db.query(UserProfile).filter(
        UserProfile.auth_user_id == profile_in.auth_user_id
    ).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Profile already exists for this user"
        )

    profile = UserProfile(**profile_in.model_dump())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

@router.get("/me", response_model=ProfileResponse)
async def get_my_profile(
    db: Session = Depends(deps.get_db),
    current_user: dict = Depends(get_current_user)
) -> ProfileResponse:
    """Get current user's profile."""
    profile = db.query(UserProfile).filter(
        UserProfile.auth_user_id == current_user["id"]
    ).first()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    return profile

@router.get("/", response_model=List[ProfileResponse])
async def get_profiles(
    db: Session = Depends(deps.get_db),
    current_user: dict = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
) -> List[ProfileResponse]:
    """Get all profiles (paginated)."""
    profiles = db.query(UserProfile).offset(skip).limit(limit).all()
    return profiles