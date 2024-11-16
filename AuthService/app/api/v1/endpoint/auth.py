from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api import deps
from app.core import security
from app.core.config import settings
from app.schemas.user import UserCreate, UserResponse, TokenResponse
from typing import Any
import logging
import uuid
from app.models.user import User, TokenInfo
from datetime import datetime

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/signup", response_model=UserResponse)
def signup(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
) -> Any:
    """
    Create new user.
    """
    user = db.query(User).filter(User.email == user_in.email).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists.",
        )
    user = User(
        email=user_in.email,
        hashed_password=security.get_password_hash(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    logger.info(f"User created successfully: {user}")
    return user


@router.post("/login", response_model=TokenResponse)
def login(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    OAuth2 compatible token login.
    """
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not security.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password",
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES) # Access token expiration time (30 minutes)
    token = security.create_access_token(user.email, expires_delta=access_token_expires) # Create access token with expiration time

    # Create token info record
    token_info = TokenInfo(
        id=str(uuid.uuid4()),
        user_id=user.id,
        access_token=token,
        expires_at=datetime.utcnow() + access_token_expires,
    )
    db.add(token_info)
    db.commit()

    logger.info(f"User logged in successfully: {user}")

    return {
        "access_token": token,
        "token_type": "bearer",
    }
