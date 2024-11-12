"""
Core configuration settings for the FastAPI application.
Loads and validates environment variables.
"""
from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from dotenv import load_dotenv

# Load environment variables from .env file
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

    class Config:
        case_sensitive = True

    def __init__(self):
        super().__init__()
        if not self.SCRAPEOPS_API_KEY:
            raise ValueError("SCRAPEOPS_API_KEY not found in environment variables")

@lru_cache
def get_settings() -> Settings:
    """
    Create and cache settings instance.
    Returns:
        Settings: Application settings
    """
    return Settings()

# Create a settings instance
settings = get_settings()