from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User, TokenInfo
from app.schemas.user import UserCreate, TokenResponse
from app.core import security
from datetime import datetime, timedelta
import uuid
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class AuthService:
    @staticmethod
    async def create_user(db: Session, user_in: UserCreate) -> User:
        """Create new user with validation."""
        logger.info("Starting user creation process")

        # Password validation already handled by pydantic schema
        # Additional check for password confirmation
        if user_in.password != user_in.password_confirm:
            logger.warning("Password confirmation failed during signup")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Passwords do not match"
            )
        
        # Validate if user exists
        if await AuthService.get_user_by_email(db, user_in.email):
            logger.warning(f"Signup attempted with existing email: {user_in.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The user with this email already exists"
            )

        try:
            user = User(
                email=user_in.email,
                hashed_password=security.get_password_hash(user_in.password),
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            
            logger.info(f"User created successfully with email: {user.email}")
            return user
            
        except Exception as e:
            logger.error(f"Error during user creation: {str(e)}")
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An error occurred while creating the user"
            )

    @staticmethod
    async def authenticate_and_create_token(
        db: Session,
        email: str,
        password: str,
    ) -> TokenResponse:
        """Authenticate user and create access token."""
        user = await AuthService.get_user_by_email(db, email)
        
        if not user or not security.verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        token = security.create_access_token(
            user.email,
            expires_delta=access_token_expires
        )

        # Create token info record
        token_info = TokenInfo(
            id=str(uuid.uuid4()),
            user_id=user.id,
            access_token=token,
            expires_at=datetime.utcnow() + access_token_expires,
        )
        db.add(token_info)
        db.commit()

        return {
            "access_token": token,
            "token_type": "bearer"
        }

    @staticmethod
    async def get_user_by_email(db: Session, email: str) -> User | None:
        """Get user by email."""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    async def delete_user(db: Session, user_id: int) -> None:
        """Delete user by ID."""
        db.query(User).filter(User.id == user_id).delete()
        db.commit()