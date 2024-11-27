
from pydantic_settings import BaseSettings
import os
from typing import Optional

class Settings(BaseSettings):
    # Project info
    PROJECT_NAME: str = "UserService"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False
    HOST: str = "0.0.0.0"
    PORT: int = 8002

    # Set defaults based on environment
    DB_USER: str = os.getenv("DB_USER", "summarizeruser" if not os.getenv("TESTING") else "test_user")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "123456" if not os.getenv("TESTING") else "test_password")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST", "localhost")
    USER_DB_NAME: str = os.getenv("USER_DB_NAME", "user_db" if not os.getenv("TESTING") else "user_test_db")
    USER_DB_PORT: str = os.getenv("USER_DB_PORT", "5433" if not os.getenv("TESTING") else "5437")
    
    # Service settings
    AUTH_SERVICE_URL: str = os.getenv("AUTH_SERVICE_URL", "http://auth_service:8001")
    AUTH_SERVICE_PORT: str = os.getenv("AUTH_SERVICE_PORT", "8001")
    USER_SERVICE_PORT: str = os.getenv("USER_SERVICE_PORT", "8002")
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
            f"{self.POSTGRES_HOST}:{self.USER_DB_PORT}/{self.USER_DB_NAME}"
        )

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"

settings = Settings()