
"""Database configuration and session management."""

from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from app.core.config import settings
import logging
import os

logger = logging.getLogger(__name__)

# Create Base class for declarative models
Base = declarative_base()

def get_engine():
    """Get database engine based on environment."""
    if os.getenv("TESTING"):
        # Use test database URL when testing
        database_url = "postgresql://test_user:test_password@localhost:5436/auth_test_db"
    else:
        # Use production database URL
        database_url = str(settings.DATABASE_URL)
        
    if not database_url:
        raise ValueError("DATABASE_URL is not configured!")

    logger.info(f"Connecting to database: {database_url}")
    
    return create_engine(
        database_url,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800,
        echo=settings.DEBUG,
    )

# Don't create engine at module level
# Instead, create it when needed
SessionLocal = None
engine = None

def init_db():
    """Initialize database engine and session factory."""
    global engine, SessionLocal
    engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)