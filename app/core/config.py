"""
Configuration settings for the summarization service.
"""

import os
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, AnyUrl

MODEL_NAME = os.getenv("MODEL_NAME", "sshleifer/distilbart-cnn-12-6")


"""
Pydantic to manage application settings. 
"""
class Settings(BaseSettings):
    PROJECT_NAME: str = "Daily Summarizer"
    PROJECT_VERSION: str = "1.0.0"
    DATABASE_URL: AnyUrl
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    class Config:
        env_file = ".env"


settings = Settings()
