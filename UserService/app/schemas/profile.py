from pydantic import BaseModel
from typing import Dict, Optional
from datetime import datetime

class ProfileCreate(BaseModel):
    """Schema for creating user profile."""
    auth_user_id: int
    full_name: Optional[str] = None
    preferences: Dict = {}
    settings: Dict = {}

class ProfileUpdate(BaseModel):
    """Schema for updating user profile."""
    full_name: Optional[str] = None
    preferences: Optional[Dict] = None
    settings: Optional[Dict] = None

class ProfileResponse(BaseModel):
    """Schema for profile response."""
    id: int
    auth_user_id: int
    full_name: Optional[str]
    preferences: Dict
    settings: Dict
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True