from UserService.app.models.profile import UserProfile
from app.schemas.user import UserProfileCreate, UserProfileUpdate
from sqlalchemy.orm import Session
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class UserService:
    """Service for managing user profiles."""

    async def create_profile(
        self, db: Session, profile: UserProfileCreate
    ) -> UserProfile:
        """Create a new user profile."""
        db_profile = UserProfile(**profile.dict())
        db.add(db_profile)
        try:
            db.commit()
            db.refresh(db_profile)
            return db_profile
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating profile: {e}")
            raise

    async def update_profile(
        self, db: Session, user_id: int, profile: UserProfileUpdate
    ) -> Optional[UserProfile]:
        """Update user profile."""
        db_profile = (
            db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        )

        if not db_profile:
            return None

        for field, value in profile.dict(exclude_unset=True).items():
            setattr(db_profile, field, value)

        try:
            db.commit()
            db.refresh(db_profile)
            return db_profile
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating profile: {e}")
            raise

    async def get_profile(self, db: Session, user_id: int) -> Optional[UserProfile]:
        """Get user profile by user_id."""
        return db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
