# app/core/config.py

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Project info
    PROJECT_NAME: str = "AuthService"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False

    # Database settings
    DB_USER: str
    DB_PASSWORD: str
    POSTGRES_HOST: str = "localhost"
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

    @property
    def get_database_url(self) -> str:
        """Get database URL from components or return configured URL."""
        if self.DATABASE_URL:
            return self.DATABASE_URL
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.POSTGRES_HOST}:{self.AUTH_DB_PORT}/{self.AUTH_DB_NAME}"

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()