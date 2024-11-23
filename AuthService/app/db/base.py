"""Database configuration and session management."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings
import logging
import os

logger = logging.getLogger(__name__)

# Create Base class for declarative models
Base = declarative_base()

# Initialize these as None initially
engine = None
SessionLocal = None

def get_database_url():
    """Get database URL based on environment."""
    if os.getenv("TESTING", "false").lower() == "true":
        return (
            f"postgresql://{os.getenv('DB_USER', 'test_user')}:"
            f"{os.getenv('DB_PASSWORD', 'test_password')}@"
            f"{os.getenv('POSTGRES_HOST', 'localhost')}:"
            f"{os.getenv('AUTH_DB_PORT', '5436')}/"
            f"{os.getenv('AUTH_DB_NAME', 'auth_test_db')}"
        )
    return settings.get_database_url

def init_db():
    """Initialize database engine and session factory."""
    global engine, SessionLocal
    
    database_url = get_database_url()
    logger.info(f"Initializing database with URL: {database_url}")
    
    engine = create_engine(
        database_url,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800,
        echo=settings.DEBUG,
    )
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Don't initialize immediately
if not os.getenv("TESTING", "false").lower() == "true":
    init_db()