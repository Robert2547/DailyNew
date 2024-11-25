import pytest
import docker
from sqlalchemy import create_engine, text


def test_docker_test_db_running():
    """Test that Docker test database container is running and accessible."""
    client = docker.from_env()
    containers = client.containers.list()

    # Check for either local docker-compose name or GitHub Actions service name
    test_db_running = any(
        "test_db" in container.name or "postgres" in container.image.tags[0]
        for container in containers
    )

    # For debugging
    if not test_db_running:
        container_info = [
            (container.name, container.image.tags) for container in containers
        ]
        print(f"Available containers: {container_info}")

    assert test_db_running, "Test database container is not running"


def test_docker_test_db_connection(test_db):
    """Test connection to Docker test database."""
    engine = create_engine(test_db)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1")).scalar()
        assert result == 1


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
