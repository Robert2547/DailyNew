from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.base import Base
""" SQLAlchemy Models for User and TokenInfo. """
class User(Base):
    """User model for storing user information."""
    
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class TokenInfo(Base):
    """Token model for storing JWT tokens."""
    
    __tablename__ = "token_info"
    
    id = Column(String, primary_key=True)
    user_id = Column(Integer, nullable=False)
    access_token = Column(String, nullable=False)
    expires_at = Column(DateTime, nullable=False)