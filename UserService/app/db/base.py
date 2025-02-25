# app/db/base.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
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
    if os.getenv("TESTING", "").lower() == "true":
        logger.info("Using test database URL")
        return "postgresql://test_user:test_password@localhost:5437/user_test_db"
    
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is not set")
    return database_url

def init_db():
    """Initialize database engine and session factory."""
    global engine, SessionLocal
    
    database_url = get_database_url()
    logger.info(f"Initializing database with URL: {database_url}")
    
    if engine is None:
        engine = create_engine(database_url)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
    return engine

def get_db():
    """Dependency for getting database session."""
    if SessionLocal is None:
        init_db()
    
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()