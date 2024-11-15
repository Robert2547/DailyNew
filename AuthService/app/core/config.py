from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, SecretStr

class Settings(BaseSettings):
    """Application configuration."""
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Auth Service"
    VERSION: str = "1.0.0"
    
    # Security
    SECRET_KEY: SecretStr
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database
    DATABASE_URL: PostgresDsn
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()