# app/core/auth.py
"""Authentication client for communicating with Auth Service."""
import httpx
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def verify_token_with_auth_service(token: str) -> dict:
    """Verify token with Auth Service."""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{settings.AUTH_SERVICE_URL}/verify-token",
                headers={"Authorization": f"Bearer {token}"},
            )
            if response.status_code == 200:
                return response.json()
            raise HTTPException(status_code=401, detail="Invalid token")
        except Exception as e:
            raise HTTPException(status_code=401, detail=str(e))


async def get_current_user(token: str = Depends(oauth2_scheme)):
    """Get current user from Auth Service."""
    return await verify_token_with_auth_service(token)
