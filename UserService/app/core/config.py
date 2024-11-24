from pydantic_settings import BaseSettings
from typing import Optional
import os
from pydantic import PostgresDsn

class Settings(BaseSettings):
    # Project info
    PROJECT_NAME: str = "UserService"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8002

    # Database settings
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "postgres")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    USER_DB_NAME: str = os.getenv("USER_DB_NAME", "user_db")
    USER_DB_PORT: str = os.getenv("USER_DB_PORT", "5433")
    
    # Auth Service settings
    AUTH_SERVICE_PORT: str = os.getenv("AUTH_SERVICE_PORT", "8001")
    AUTH_DB_NAME: str = os.getenv("AUTH_DB_NAME", "auth_db")
    AUTH_DB_PORT: str = os.getenv("AUTH_DB_PORT", "5432")
    USER_SERVICE_PORT: str = os.getenv("USER_SERVICE_PORT", "8002")
    USER_SERVICE_URL: str = os.getenv("USER_SERVICE_URL", "http://localhost:8002")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-here")
    
    # Service URLs
    AUTH_SERVICE_URL: str = os.getenv("AUTH_SERVICE_URL", "http://auth_service:8001")

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Allow extra fields from env file

    def get_database_url(self) -> str:
        """Get database URL based on environment."""
        if os.getenv("TESTING", "false").lower() == "true":
            return (
                f"postgresql://{os.getenv('DB_USER', 'test_user')}:"
                f"{os.getenv('DB_PASSWORD', 'test_password')}@"
                f"{os.getenv('POSTGRES_HOST', 'localhost')}:"
                f"{os.getenv('USER_DB_PORT', '5437')}/"
                f"{os.getenv('USER_DB_NAME', 'user_test_db')}"
            )
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.POSTGRES_HOST}:{self.USER_DB_PORT}/{self.USER_DB_NAME}"
        )

settings = Settings()