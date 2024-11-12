"""
API dependencies including authentication and common dependencies
"""
from fastapi import Depends, HTTPException, status
from fastapi.security.api_key import APIKeyHeader
from typing import Optional
from app.core.config import settings

# Initialize API Key header checker
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def verify_api_key(api_key: Optional[str] = Depends(api_key_header)) -> str:
    """
    Verify the API key provided in request headers against SCRAPEOPS_API_KEY.
    
    Args:
        api_key (Optional[str]): API key from request header
        
    Returns:
        str: Verified API key
        
    Raises:
        HTTPException: If API key is missing or invalid
    """
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API Key header is missing",
            headers={"WWW-Authenticate": API_KEY_NAME},
        )
        
    if api_key != settings.SCRAPEOPS_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API key provided",
            headers={"WWW-Authenticate": API_KEY_NAME},
        )
        
    return api_key

async def get_proxy_url() -> str:
    """
    Get the proxy URL for scraping operations.
    
    Returns:
        str: Configured proxy URL
    """
    return settings.PROXY_URL