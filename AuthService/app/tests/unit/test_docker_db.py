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
        'test_db' in container.name  # More flexible matching
        for container in containers
    )
    
    # Add debugging information
    if not test_db_running:
        container_names = [container.name for container in containers]
        print(f"Available containers: {container_names}")
    
    assert test_db_running, "Test database container is not running"

def test_docker_test_db_connection(test_db):
    """Test connection to Docker test database."""
    try:
        # Create engine
        engine = create_engine(test_db)
        
        # Try a simple query
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1")).scalar()
            
        assert result == 1, "Database query failed"
        
    except Exception as e:
        pytest.fail(f"Failed to connect to Docker test database: {str(e)}")

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