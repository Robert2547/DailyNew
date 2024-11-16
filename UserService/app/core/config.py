from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, AnyUrl, Field

class Settings(BaseSettings):
    """User service configuration."""
    
    PROJECT_NAME: str = "User Service"
    VERSION: str = "1.0.0"
    HOST: str = "0.0.0.0"
    PORT: int = 8003
    
    # Database for user-specific data
    DATABASE_URL: PostgresDsn
    
    # Auth Service connection
    AUTH_SERVICE_URL: AnyUrl
    
    class Config:
        env_file = ".env"