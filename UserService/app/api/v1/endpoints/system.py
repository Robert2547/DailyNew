from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from sqlalchemy import text
import logging, os
from typing import Dict, Any

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/health-check")
async def health_check() -> Dict[str, Any]:
    """Check if service is running and database is connected."""
    try:
        # Test database connection
        db = next(deps.get_db())
        test_query = text("SELECT 1")
        db.execute(test_query).scalar()

        return {
            "status": "healthy",
            "service": "auth-service",
            "database": "connected",
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "unhealthy",
            "service": "auth-service",
            "database": "disconnected",
            "error": str(e),
        }
