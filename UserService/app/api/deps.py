from fastapi import Depends, HTTPException
from app.core.auth import verify_token_with_auth_service
from fastapi.security import OAuth2PasswordBearer
from app.db.base import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    return await verify_token_with_auth_service(token)
