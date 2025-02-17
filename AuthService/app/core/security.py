from datetime import datetime, timedelta
from typing import Any, Optional, Union
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings
from pydantic import SecretStr

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)


def get_secret_key(secret: Union[str, SecretStr]) -> str:
    """Get secret key string from either str or SecretStr."""
    if isinstance(secret, SecretStr):
        return secret.get_secret_value()
    return secret


def create_access_token(
    subject: Union[str, Any],
    user_id: int,  # Add this parameter
    expires_delta: Optional[timedelta] = None,
) -> str:
    """Create JWT access token."""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "user_id": user_id,  # Include user_id in token
    }
    encoded_jwt = jwt.encode(
        to_encode, get_secret_key(settings.SECRET_KEY), algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plain and hashed password match."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Generate password hash."""
    return pwd_context.hash(password)


def verify_token(token: str) -> Optional[str]:
    """Verify JWT token."""
    try:
        payload = jwt.decode(
            token, get_secret_key(settings.SECRET_KEY), algorithms=[settings.ALGORITHM]
        )
        return payload
    except jwt.JWTError:
        return None
