from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import logging
import time
from typing import Optional

logger = logging.getLogger(__name__)


def check_db_connection(database_url: str, retries: int = 5, delay: int = 2) -> bool:
    """
    Check if database is accessible with retries.

    Args:
        database_url: SQLAlchemy database URL
        retries: Number of connection attempts
        delay: Delay between retries in seconds

    Returns:
        bool: True if connection successful, False otherwise
    """
    for attempt in range(retries):
        try:
            # Create temporary engine for testing
            engine = create_engine(database_url)

            # Test connection with simple query
            with engine.connect() as connection:
                connection.execute(text("SELECT 1"))

            logger.info("Successfully connected to the database")
            return True

        except SQLAlchemyError as e:
            logger.warning(
                f"Database connection attempt {attempt + 1} failed: {str(e)}"
            )
            if attempt < retries - 1:
                time.sleep(delay)
                continue
            else:
                logger.error("Failed to connect to database after all retries")
                return False
        finally:
            if "engine" in locals():
                engine.dispose()

    return False
