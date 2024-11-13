"""
Core configuration settings for the FastAPI application.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    # API Keys and URLs
    SCRAPEOPS_API_KEY: str = os.getenv("SCRAPEOPS_API_KEY")
    PROXY_URL: str = "https://proxy.scrapeops.io/v1/"
    
    # API Settings
    APP_NAME: str = "Financial News Scraper API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "API for scraping financial news from multiple sources"
    
    # CORS Settings
    ALLOWED_ORIGINS: list = ["*"]

    # Optional Redis Settings
    USE_REDIS: bool = False  # Set to True if you want to use Redis
    REDIS_HOST: str = "localhost"  # Only used if USE_REDIS is True
    REDIS_PORT: int = 6379
    CACHE_EXPIRATION: int = 300  # 5 minutes

    class Config:
        case_sensitive = True

    def __init__(self):
        super().__init__()
        if not self.SCRAPEOPS_API_KEY:
            raise ValueError("SCRAPEOPS_API_KEY not found in environment variables")

@lru_cache
def get_settings() -> Settings:
    return Settings()

# Create a settings instance
settings = get_settings()