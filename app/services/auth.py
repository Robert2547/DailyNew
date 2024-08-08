from sqlalchemy.orm import Session
from app.models.user import User
from passlib.context import CryptContext
from app.schemas.user import UserCreate
import logging
from fastapi import HTTPException, status
from datetime import timedelta, datetime
from jose import JWTError
from jose import jwt
from typing import Optional
from sqlalchemy.exc import SQLAlchemyError
from pydantic.networks import EmailStr
from app.core import settings
import uuid
from app.models.user import TokenInfo

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT settings
SECRET_KEY = settings.SECRET_KEY.get_secret_value()
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

def get_user(db: Session, email: str):
    """
    Retrieve a user from the database by email.

    Args:
        db (Session): The database session.
        email (str): The email of the user to retrieve.

    Returns:
        User: The user object if found, else None.
    """
    try:
        return db.query(User).filter(User.email == email).first()
    except Exception as e:
        logger.error(f"Database error when retrieving user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


def create_user(db: Session, user: UserCreate):
    """
    Create a new user in the database.

    Args:
        db (Session): The database session.
        user (UserCreate): The user data to create.

    Returns:
        User: The created user object.
    """
    try:
        if get_user(db, user.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered",
            )

        hashed_password = pwd_context.hash(user.password)
        db_user = User(email=user.email, hashed_password=hashed_password)
        db.add(db_user)
        logger.info(f"User created successfully: {user.email}")
        return db_user
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user",
        )

def create_token(db: Session, user: User):
    """
    Create a new access token for the user in the database.

    Args:
        db (Session): The database session.
        user (User): The user object.

    Returns:
        TokenInfo: The created token object.
    """
    try:
        token_info = TokenInfo(
            id=str(uuid.uuid4()),
            user_id=user.id,
            access_token=create_access_token(data={"sub": user.email}),
            expires_at=datetime.utcnow() + timedelta(minutes=30),
        )
        db.add(token_info)
        logger.info(f"Token created successfully for user: {user.email}")
        return token_info
    except Exception as e:
        logger.error(f"Error creating token: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating token",
        )
    

def authenticate_user(db: Session, email: str, password: str):
    """
    Authenticate a user by verifying their email and password.

    Args:
        db (Session): The database session.
        email (str): The email of the user to authenticate.
        password (str): The password to verify.

    Returns:
        User: The authenticated user object if successful, else None.
    """
    user = get_user(db, email)
    if not user or not pwd_context.verify(password, user.hashed_password): 
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return user

# Good
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a JWT access token for authenticated users.

    Args:
        data (dict): The payload to encode in the token.
        expires_delta (Optional[timedelta]): The token expiration time.

    Returns:
        str: The encoded JWT token.

    Raises:
        HTTPException: If token creation fails.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    try:
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except JWTError as e:
        logger.error(f"Error creating access token: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create access token",
        )


def verify_token(token: str) -> dict:
    """
    Verify and decode a JWT token.

    Args:
        token (str): The JWT token to verify and decode.

    Returns:
        dict: The decoded token payload.

    Raises:
        HTTPException: If token validation fails.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        logger.error(f"Error verifying token: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(db: Session, token: str) -> User:
    """
    Retrieve the current user from the database using the JWT.

    Args:
        db (Session): The database session.
        token (str): The JWT token.

    Returns:
        User: The current user.

    Raises:
        HTTPException: If user retrieval fails.
    """
    payload = verify_token(token)
    email: str = payload.get("sub")
    if email is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    user = get_user(db, email)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return user


def create_password_reset_token(db: Session, email: EmailStr) -> str:
    """
    Create a password reset token for the user.

    Args:
        db (Session): The database session.
        email (EmailStr): The email of the user requesting password reset.

    Returns:
        str: The password reset token.

    Raises:
        HTTPException: If user is not found or token creation fails.
    """
    user = get_user(db, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    token_data = {
        "sub": user.email,
        "type": "password_reset",
        "exp": datetime.utcnow() + timedelta(hours=1),
    }
    return create_access_token(token_data)


def reset_password(db: Session, token: str, new_password: str) -> bool:
    """
    Reset the user's password using the password reset token.

    Args:
        db (Session): The database session.
        token (str): The password reset token.
        new_password (str): The new password to set.

    Returns:
        bool: True if password reset was successful.

    Raises:
        HTTPException: If token is invalid, user is not found, or password reset fails.
    """
    try:
        payload = verify_token(token)
        if payload.get("type") != "password_reset":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token type"
            )
        user = get_user(db, payload.get("sub"))
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )
        user.hashed_password = pwd_context.hash(new_password)
        db.commit()
        logger.info(f"Password reset successfully for user: {user.email}")
        return True
    except JWTError as e:
        logger.error(f"Error resetting password (invalid token): {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid or expired token"
        )
    except SQLAlchemyError as e:
        logger.error(f"Database error when resetting password: {e}")
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error resetting password",
        )
