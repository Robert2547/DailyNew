"""
Configuration settings for the summarization service.
"""
from pydantic_settings import BaseSettings
from pydantic import AnyUrl, SecretStr, Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "Daily Summarizer"
    PROJECT_VERSION: str = "1.0.0"
    
    # Service URLs
    AUTH_SERVICE_URL: AnyUrl  # URL for the auth microservice
    DATABASE_URL: AnyUrl
    
    # API Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Model Settings
    MODEL_NAME: str = "sshleifer/distilbart-cnn-12-6"
    
    # Debug mode
    DEBUG: bool = Field(default=False)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()