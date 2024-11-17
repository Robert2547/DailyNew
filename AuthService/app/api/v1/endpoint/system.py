from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api import deps
from sqlalchemy import text
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/test-connection")
def test_connection(db: Session = Depends(deps.get_db)) -> Dict[str, Any]:
    """Test database connection."""
    logger.info("Testing database connection")
    try:
        # Simplest possible query
        stmt = text("SELECT 1")
        result = db.execute(stmt).scalar()
        
        if result == 1:
            info_stmt = text("""
                SELECT 
                    CAST(current_database() as VARCHAR) as db,
                    CAST(current_user as VARCHAR) as usr
            """)
            
            db_info = db.execute(info_stmt).fetchone()
            
            response = {
                "status": "connected",
                "database": str(db_info[0]),
                "user": str(db_info[1]),
                "database_url": str(deps.settings.DATABASE_URL)
            }
            
            logger.info(f"Successful response: {response}")
            return response
            
    except Exception as e:
        error_response = {
            "status": "error",
            "error": str(e),
            "database_url": str(deps.settings.DATABASE_URL)
        }
        logger.error(f"Error response: {error_response}")
        return error_response