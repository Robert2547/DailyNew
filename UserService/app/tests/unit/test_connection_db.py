import pytest
from app.utils.db_utils import check_db_connection
import logging
from sqlalchemy import create_engine, text

logger = logging.getLogger(__name__)


def test_database_connection(setup_test_env):
    """Test basic database connection."""
    database_url = "postgresql://test_user:test_password@localhost:5437/user_test_db"
    engine = create_engine(database_url)

    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        value = result.scalar()
        assert value == 1


def test_database_connection_invalid_url():
    """Test failed database connection."""
    invalid_url = "postgresql://invalid:invalid@localhost:5432/invalid_db"
    assert check_db_connection(invalid_url) is False
