from sqlalchemy.orm import Session
from app.models.profile import UserProfile
from app.schemas.profile import ProfileCreate, ProfileUpdate
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class ProfileService:
    def __init__(self, db: Session):
        self.db = db
        
    async def create_profile(self, profile: ProfileCreate) -> UserProfile:
        """Create a new user profile."""
        db_profile = UserProfile(**profile.dict())
        self.db.add(db_profile)
        try:
            self.db.commit()
            self.db.refresh(db_profile)
            return db_profile
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error creating profile: {e}")
            raise
            
    async def get_profile_by_auth_id(self, auth_user_id: int) -> Optional[UserProfile]:
        """Get profile by auth service user ID."""
        return self.db.query(UserProfile).filter(
            UserProfile.auth_user_id == auth_user_id
        ).first()
        
    async def update_profile(
        self, auth_user_id: int, profile_data: ProfileUpdate
    ) -> Optional[UserProfile]:
        """Update user profile."""
        profile = await self.get_profile_by_auth_id(auth_user_id)
        if not profile:
            return None
            
        for field, value in profile_data.dict(exclude_unset=True).items():
            setattr(profile, field, value)
            
        try:
            self.db.commit()
            self.db.refresh(profile)
            return profile
        except Exception as e:
            self.db.rollback()
            logger.error(f"Error updating profile: {e}")
            raise