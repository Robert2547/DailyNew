"""Models specific to user profiles and preferences."""
from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.db.base import Base

class UserProfile(Base):
    """Extended user profile information."""
    
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True)
    auth_user_id = Column(Integer, unique=True, nullable=False)  # References Auth Service user ID
    full_name = Column(String)
    preferences = Column(JSON, default={})
    settings = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())