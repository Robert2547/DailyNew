"""Pydantic models for request/response handling."""

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    """Base user schema with common attributes."""
    email: EmailStr = Field(..., description="User email address")

class UserCreate(UserBase):
    """Schema for user creation."""
    password: str = Field(
        ..., 
        min_length=8,
        description="User password (min 8 characters)"
    )

class UserUpdate(BaseModel):
    """Schema for user updates."""
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None

class UserInDBBase(UserBase):
    """Base schema for user in database."""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class User(UserInDBBase):
    """Schema for user responses."""
    pass

class UserInDB(UserInDBBase):
    """Schema for user in database (includes hashed password)."""
    hashed_password: str

class TokenResponse(BaseModel):
    """Schema for token response."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Schema for token payload."""
    email: Optional[str] = None
