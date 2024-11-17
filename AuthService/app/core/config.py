from pydantic_settings import BaseSettings
from pydantic import PostgresDsn, AnyUrl

class Settings(BaseSettings):
    PROJECT_NAME: str = "Auth Service"
    VERSION: str = "1.0.0"
    
    # Database
    DATABASE_URL: PostgresDsn
    
    # JWT
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Service URLs
    USER_SERVICE_URL: AnyUrl
    
    class Config:
        env_file = ".env"

settings = Settings()