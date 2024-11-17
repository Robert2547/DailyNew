from datetime import timedelta
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.api import deps
from app.core.config import settings
from app.schemas.user import UserCreate, UserResponse, TokenResponse
from typing import Any
import logging
import httpx
from app.services.auth_service import AuthService
from fastapi import HTTPException


logger = logging.getLogger(__name__)
router = APIRouter()


@router.post(
    "/signup",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    description="Create new user account",
)
async def signup(
    *,
    db: Session = Depends(deps.get_db),
    user_in: UserCreate,
) -> Any:
    """Create new user and corresponding profile in UserService."""
    # Create auth user
    auth_user = await AuthService.create_user(db, user_in)

    # Create user profile in UserService
    try:
        async with httpx.AsyncClient() as client:
            profile_response = await client.post(
                f"{settings.USER_SERVICE_URL}/api/v1/profiles/",
                json={"auth_user_id": auth_user.id, "email": auth_user.email},
            )
            if profile_response.status_code != 201:
                # Rollback auth user creation if profile creation fails
                await AuthService.delete_user(db, auth_user.id)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to create user profile",
                )
    except Exception as e:
        await AuthService.delete_user(db, auth_user.id)
        logger.error(f"Error creating user profile: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user profile",
        )

    return auth_user


@router.post(
    "/login", response_model=TokenResponse, description="OAuth2 compatible token login"
)
async def login(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """Authenticate user and return token."""
    token_data = await AuthService.authenticate_and_create_token(
        db, form_data.username, form_data.password
    )

    logger.info(f"User logged in successfully: {form_data.username}")
    return token_data


@router.post("/verify-token")
async def verify_token(current_user: Any = Depends(deps.get_current_user)) -> Any:
    """Verify token and return user info."""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "is_active": current_user.is_active,
    }
