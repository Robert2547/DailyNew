# app/core/config.py

from pydantic_settings import BaseSettings
from typing import Optional
import os
from pydantic import SecretStr
import logging

logger = logging.getLogger(__name__)

class Settings(BaseSettings):
    # Project info
    PROJECT_NAME: str = "AuthService"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False

    # Database settings
    DB_USER: str = os.getenv("DB_USER", "defaultuser")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "defaultpassword")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    AUTH_DB_NAME: str = "auth_db"
    AUTH_DB_PORT: str = "5432"
    USER_DB_NAME: str = "user_db"
    USER_DB_PORT: str = "5433"

    # Service settings
    AUTH_SERVICE_PORT: str = "8001"
    USER_SERVICE_PORT: str = "8002"
    USER_SERVICE_URL: str = "http://user_service:8002"

    # Auth settings
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Database URL (constructed from components)
    DATABASE_URL: Optional[str] = None

    SECRET_KEY: SecretStr
    ALGORITHM: str = "HS256"
    @property
    def get_database_url(self) -> str:
        """Get database URL based on environment."""
        # First check if we're in test mode
        if os.getenv("TESTING", "false").lower() == "true":
            # Check if we're running in Docker or locally
            test_host = "test_db" if os.getenv("IN_DOCKER", "false").lower() == "true" else "localhost"
            test_port = "5432" if os.getenv("IN_DOCKER", "false").lower() == "true" else "5436"
            url = f"postgresql://test_user:test_password@{test_host}:{test_port}/auth_test_db"
            logger.info(f"Using test database URL: {url}")
            return url
        
        # Default case: construct URL from settings
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.POSTGRES_HOST}:{self.AUTH_DB_PORT}/{self.AUTH_DB_NAME}"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
