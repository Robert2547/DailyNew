from pydantic_settings import BaseSettings
import os
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    # Project info
    PROJECT_NAME: str = "WatchlistService"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8003

    # Database settings
    DB_USER: str = os.getenv(
        "DB_USER", "watchlistuser" if not os.getenv("TESTING") else "test_user"
    )
    DB_PASSWORD: str = os.getenv(
        "DB_PASSWORD", "123456" if not os.getenv("TESTING") else "test_password"
    )
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    WATCHLIST_DB_NAME: str = os.getenv(
        "WATCHLIST_DB_NAME",
        "watchlist_db" if not os.getenv("TESTING") else "watchlist_test_db",
    )
    WATCHLIST_DB_PORT: str = os.getenv(
        "WATCHLIST_DB_PORT", "5434" if not os.getenv("TESTING") else "5438"
    )

    # Service settings
    AUTH_SERVICE_URL: str = os.getenv("AUTH_SERVICE_URL", "http://auth_service:8001")
    USER_SERVICE_URL: str = os.getenv("USER_SERVICE_URL", "http://user_service:8002")
    AUTH_SERVICE_PORT: str = os.getenv("AUTH_SERVICE_PORT", "8001")
    USER_SERVICE_PORT: str = os.getenv("USER_SERVICE_PORT", "8002")
    WATCHLIST_SERVICE_PORT: str = os.getenv("WATCHLIST_SERVICE_PORT", "8003")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")

    # Database URL (constructed from components)
    DATABASE_URL: Optional[str] = None

    def get_database_url(self) -> str:
        """Get database URL based on environment."""
        # Use the environment DATABASE_URL if provided
        if os.getenv("DATABASE_URL"):
            return os.getenv("DATABASE_URL")

        # Otherwise construct from components
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.WATCHLIST_DB_PORT}/{self.WATCHLIST_DB_NAME}"
        )

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"


settings = Settings()
