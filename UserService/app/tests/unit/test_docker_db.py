import pytest
import docker
from sqlalchemy import create_engine, text


def test_docker_test_db_running():
    """Test that Docker test database container is running and accessible."""
    # Get Docker client
    client = docker.from_env()

    # Check if test_db container is running
    containers = client.containers.list()
    test_db_running = any(
        "test_db" in container.name  # More flexible matching
        for container in containers
    )

    # Add debugging information
    if not test_db_running:
        container_names = [container.name for container in containers]
        print(f"Available containers: {container_names}")

    assert test_db_running, "Test database container is not running"


def test_docker_test_db_connection(setup_test_env):
    """Test connection to Docker test database."""
    database_url = "postgresql://test_user:test_password@localhost:5437/user_test_db"
    engine = create_engine(database_url)

    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        assert result.scalar() == 1


def test_docker_test_db_credentials(setup_test_env):
    """Test database credentials and permissions."""
    database_url = "postgresql://test_user:test_password@localhost:5437/user_test_db"
    engine = create_engine(database_url)

    with engine.connect() as conn:
        # Test write permission by creating and dropping a table
        conn.execute(
            text(
                """
            CREATE TABLE IF NOT EXISTS test_permissions (
                id SERIAL PRIMARY KEY,
                name TEXT
            )
        """
            )
        )
        conn.execute(text("DROP TABLE test_permissions"))
        assert True  # If we got here, the permissions work
