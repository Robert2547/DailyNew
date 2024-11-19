# app/core/test_config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Any

class TestSettings(BaseSettings):
    # Project info
    PROJECT_NAME: str = "AuthService Test"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True

    # Database settings
    DB_USER: str = "test_user"
    DB_PASSWORD: str = "test_password"
    POSTGRES_HOST: str = "localhost"
    AUTH_DB_PORT: int = 5436
    AUTH_DB_NAME: str = "auth_test_db"
    
    # Database URL
    DATABASE_URL: str = f"postgresql://{DB_USER}:{DB_PASSWORD}@{POSTGRES_HOST}:{AUTH_DB_PORT}/{AUTH_DB_NAME}"

    # Service URLs
    USER_SERVICE_URL: str = "http://localhost:8002"
    
    # Auth settings
    SECRET_KEY: str = "test_secret_key_super_secret_for_testing"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Test user credentials
    TEST_USER_EMAIL: str = "pytest@example.com"
    TEST_USER_PASSWORD: str = "test_password123"

    # Using SettingsConfigDict instead of config class
    model_config = SettingsConfigDict(
        env_file=".env.test",
        case_sensitive=True,
        extra="allow"
    )

test_settings = TestSettings()