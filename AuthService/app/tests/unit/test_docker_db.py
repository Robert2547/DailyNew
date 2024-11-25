import pytest
import docker
from sqlalchemy import create_engine, text

def test_docker_test_db_running():
    """Test that Docker test database container is running and accessible."""
    client = docker.from_env()
    containers = client.containers.list()
    
    # Check for either local docker-compose name or GitHub Actions service name
    test_db_running = any(
        'test_db' in container.name or 
        'postgres' in container.image.tags[0]
        for container in containers
    )
    
    # For debugging
    if not test_db_running:
        container_info = [(container.name, container.image.tags) for container in containers]
        print(f"Available containers: {container_info}")
        
    assert test_db_running, "Test database container is not running"

def test_docker_test_db_connection(test_db):
    """Test connection to Docker test database."""
    engine = create_engine(test_db)
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1")).scalar()
        assert result == 1

def test_docker_test_db_credentials(test_db):
    """Test that Docker test database credentials are correct."""
    engine = create_engine(test_db)
    
    with engine.connect() as conn:
        # Check current database name
        db_name = conn.execute(
            text("SELECT current_database()")
        ).scalar()
        assert db_name == "auth_test_db"
        
        # Check current user
        user = conn.execute(
            text("SELECT current_user")
        ).scalar()
        assert user == "test_user"