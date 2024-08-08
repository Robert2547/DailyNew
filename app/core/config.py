"""
Configuration settings for the summarization service.
"""

import os
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, AnyUrl, SecretStr, Field

MODEL_NAME = os.getenv("MODEL_NAME", "sshleifer/distilbart-cnn-12-6")


class Settings(BaseSettings):
    PROJECT_NAME: str = "Daily Summarizer"
    PROJECT_VERSION: str = "1.0.0"
    DATABASE_URL: AnyUrl
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # JWT settings
    SECRET_KEY: SecretStr
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # Debug mode
    DEBUG: bool = Field(default=False)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


settings = Settings()
