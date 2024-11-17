from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.api import deps
from app.models.profile import UserProfile
from app.schemas.profile import ProfileCreate, ProfileUpdate, ProfileResponse
from app.core.auth import get_current_user
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", response_model=ProfileResponse)
async def create_profile(
    profile_in: ProfileCreate,
    db: Session = Depends(deps.get_db),
    current_user: dict = Depends(get_current_user)
) -> ProfileResponse:
    """
    Create a new user profile.
    """
    logger.info(f"Creating profile for auth_user_id: {profile_in.auth_user_id}")
    
    # Check if profile already exists
    existing_profile = db.query(UserProfile).filter(
        UserProfile.auth_user_id == profile_in.auth_user_id
    ).first()
    
    if existing_profile:
        raise HTTPException(
            status_code=400,
            detail="Profile already exists for this user"
        )
    
    profile = UserProfile(**profile_in.model_dump())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

@router.get("/", response_model=List[ProfileResponse])
async def get_profiles(
    db: Session = Depends(deps.get_db),
    current_user: dict = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100
) -> List[ProfileResponse]:
    """
    Retrieve all user profiles with pagination.
    """
    logger.info(f"Fetching profiles with skip={skip} and limit={limit}")
    profiles = db.query(UserProfile).offset(skip).limit(limit).all()
    return profiles

@router.get("/me", response_model=ProfileResponse)
async def get_my_profile(
    db: Session = Depends(deps.get_db),
    current_user: dict = Depends(get_current_user)
) -> ProfileResponse:
    """
    Get current user's profile.
    """
    logger.info(f"Fetching profile for auth_user_id: {current_user['id']}")
    profile = db.query(UserProfile).filter(
        UserProfile.auth_user_id == current_user['id']
    ).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.get("/{profile_id}", response_model=ProfileResponse)
async def get_profile(
    profile_id: int,
    db: Session = Depends(deps.get_db),
    current_user: dict = Depends(get_current_user)
) -> ProfileResponse:
    """
    Get profile by ID.
    """
    logger.info(f"Fetching profile with id={profile_id}")
    profile = db.query(UserProfile).filter(UserProfile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.put("/me", response_model=ProfileResponse)
async def update_my_profile(
    profile_update: ProfileUpdate,
    db: Session = Depends(deps.get_db),
    current_user: dict = Depends(get_current_user)
) -> ProfileResponse:
    """
    Update current user's profile.
    """
    profile = db.query(UserProfile).filter(
        UserProfile.auth_user_id == current_user['id']
    ).first()
    
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    update_data = profile_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(profile, field, value)
    
    db.commit()
    db.refresh(profile)
    return profile

@router.get("/by-auth-id/{auth_user_id}", response_model=ProfileResponse)
async def get_profile_by_auth_id(
    auth_user_id: int,
    db: Session = Depends(deps.get_db),
    current_user: dict = Depends(get_current_user)
) -> ProfileResponse:
    """
    Get profile by auth user ID.
    """
    logger.info(f"Fetching profile for auth_user_id={auth_user_id}")
    profile = db.query(UserProfile).filter(
        UserProfile.auth_user_id == auth_user_id
    ).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile