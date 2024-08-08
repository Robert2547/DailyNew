from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.services.auth import create_user, authenticate_user, create_token
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import UserCreate, UserInDB, UserResponse, UserLogin
from datetime import timedelta
from app.services.auth import (
    create_access_token,
    create_password_reset_token,
    reset_password,
)
import logging
from datetime import datetime
import uuid
from app.db.base import get_db
from app.models.user import TokenInfo


router = APIRouter()
logger = logging.getLogger(__name__)


@router.post(
    "/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    """
    Create a new user account.

    Args:
        user (UserResponse): The user data to create. (ID, user, access_token, token_type)
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If a user with the given email already exists.

    Returns:
        UserInDB: The created user object.
    """
    db_user = create_user(db, user)
    if not db_user:  # User already exists
        raise HTTPException(status_code=400, detail="Email already registered")

    token_info = create_token(db, db_user)  # Create a new token
    if token_info is None:
        raise HTTPException(status_code=500, detail="Token creation failed")

    try:
        db.commit()
        user_in_db = UserInDB.model_validate(
            db_user
        )  # Convert the SQLAlchemy model to Pydantic model
    except Exception as e:
        logger.error(f"Error creating token: {e}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Token creation failed")
    return UserResponse(
        id=user_in_db.id,
        user=user_in_db,
        access_token=token_info.access_token,
        token_type="bearer",
    )


@router.post("/login", response_model=UserResponse)
def login(login_request: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate a user and log them in.

    Args:
        login_request (UserLogin): The user login credentials.
        db (Session, optional): The database session. Defaults to Depends(get_db).

    Raises:
        HTTPException: If the login credentials are invalid.

    Returns:
        returns a UserResponse with the access token and token type.
    """
    user = authenticate_user(db, login_request.email, login_request.password)
    if not user:  # No user found
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Check if the user has a valid token
    token_info = (
        db.query(TokenInfo)
        .filter(TokenInfo.user_id == user.id)
        .order_by(TokenInfo.expires_at.desc())
        .first()
    )
    if (
        not token_info or token_info.expires_at < datetime.now()
    ):  # No token found or token expired
        token_info = TokenInfo(  # Create a new token
            id=str(uuid.uuid4()),
            user_id=user.id,
            access_token=create_access_token(data={"sub": user.email}),
            expires_at=datetime.utcnow() + timedelta(minutes=30),
        )
        db.add(token_info)
        db.commit()

    return UserResponse(
        id=user.id, user=user, access_token=token_info.access_token, token_type="bearer"
    )


@router.post("/password-reset-request")
async def request_password_reset(email: str, db: Session = Depends(get_db)):
    token = create_password_reset_token(db, email)
    # Here you would typically send an email with the reset token
    return {
        "message": "If the email exists in our system, a password reset link has been sent."
    }


@router.post("/password-reset")
async def perform_password_reset(
    token: str, new_password: str, db: Session = Depends(get_db)
):
    if reset_password(db, token, new_password):
        return {"message": "Password reset successfully"}
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="Password reset failed"
    )
