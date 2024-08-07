"""
This will contain our database connection setup.
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Create the SQLAlchemy engine
engine = create_engine(str(settings.DATABASE_URL), pool_pre_ping=True)

# Create a SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for declarative models
Base = declarative_base()


# Dependency
def get_db():
    """
    Dependency function to get a database session.

    Yields:
        Session: A SQLAlchemy database session.

    Note:
        This function should be used as a FastAPI dependency to ensure
        that database sessions are properly managed and closed after each request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
