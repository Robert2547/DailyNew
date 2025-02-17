from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_token(token: str):
    try:
        # Add debug logging
        logger.info(f"Actual token being verified: {token}")
        logger.info(
            f"Secret key being used: {settings.SECRET_KEY[:5]}..."
        )  # Show first 5 chars only for security

        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        email = payload.get("sub")
        if not email:
            raise ValueError("Email not found in token")
        return payload
    except JWTError as e:
        logger.error(f"Token validation error: {str(e)}")
        raise ValueError(f"Invalid token: {str(e)}")


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=["HS256"],
            options={"verify_exp": False},
        )

        user_id = payload.get("user_id")
        if not user_id:
            raise ValueError("User ID not found in token")

        return {
            "id": user_id,  # This will now be the numeric ID
            "email": payload.get("sub"),
            "exp": payload.get("exp"),
        }
    except Exception as e:
        logger.error(f"Authentication error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
