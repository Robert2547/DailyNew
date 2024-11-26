"""Pydantic models for request/response handling."""

from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
import re


class PasswordMixin(BaseModel):
    """Mixin for password validation rules."""

    password: str = Field(
        ...,
        min_length=8,
        description="Password must be at least 8 characters long and contain uppercase, lowercase, number",
    )

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        """Validate password meets strength requirements."""
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least one number")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", v):
            raise ValueError("Password must contain at least one special character")
        return v


class UserBase(BaseModel):
    """Base user schema with common attributes."""

    email: EmailStr = Field(
        ..., description="User email address", examples=["user@example.com"]
    )

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Normalize email to lowercase."""
        return v.lower()


class UserCreate(UserBase, PasswordMixin):
    """Schema for user creation."""

    password_confirm: str = Field(
        ..., min_length=8, description="Confirm password (must match password)"
    )

    @field_validator("password_confirm")
    @classmethod
    def passwords_match(cls, v: str, info) -> str:
        """Validate password and password_confirm match."""
        if "password" in info.data and v != info.data["password"]:
            raise ValueError("Passwords do not match")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "user@example.com",
                "password": "StrongPass123!",
                "password_confirm": "StrongPass123!",
            }
        }
    }


class UserUpdate(BaseModel):
    """Schema for user updates."""

    email: Optional[EmailStr] = Field(None, description="Updated email address")
    is_active: Optional[bool] = Field(None, description="User active status")

    @field_validator("email")
    @classmethod
    def validate_optional_email(cls, v: Optional[str]) -> Optional[str]:
        """Normalize email to lowercase if provided."""
        if v:
            return v.lower()
        return v


class UserInDBBase(UserBase):
    """Base schema for user in database."""

    id: int = Field(..., description="Unique user identifier")
    is_active: bool = Field(..., description="User active status")
    created_at: datetime = Field(..., description="Account creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    model_config = {"from_attributes": True}


class UserResponse(UserInDBBase):
    """Schema for user responses."""

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": 1,
                "email": "user@example.com",
                "is_active": True,
                "created_at": "2024-11-17T10:00:00",
                "updated_at": "2024-11-17T10:30:00",
            }
        }
    }


class UserInDB(UserInDBBase):
    """Schema for user in database (includes hashed password)."""

    hashed_password: str = Field(..., description="Hashed user password")


class TokenResponse(BaseModel):
    """Schema for token response."""

    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(..., description="Token type (e.g., 'bearer')")

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
            }
        }
    }


class TokenData(BaseModel):
    """Schema for token payload."""

    email: Optional[str] = Field(None, description="User email from token")

    model_config = {"json_schema_extra": {"example": {"email": "user@example.com"}}}


class LoginRequest(BaseModel):
    """Schema for login request"""

    email: EmailStr
    password: str
