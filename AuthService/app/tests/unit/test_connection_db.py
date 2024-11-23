import pytest
from app.utils.db_utils import check_db_connection
import logging

logger = logging.getLogger(__name__)

def test_database_connection(test_db):
    """Test database connection is successful."""
    logger.info(f"Testing connection to database: {test_db}")
    
    # Attempt connection with test database URL
    is_connected = check_db_connection(test_db)
    
    # Add debugging information
    if not is_connected:
        logger.error(f"Failed to connect to test database: {test_db}")
        
    # Assert connection was successful
    assert is_connected is True

def test_database_connection_invalid_url():
    """Test failed database connection."""
    invalid_url = "postgresql://invalid:invalid@localhost:5432/invalid_db"
    assert check_db_connection(invalid_url) is False