from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Summarizer service configuration."""

    # Service Info
    PROJECT_NAME: str = "Summarizer Service"
    VERSION: str = "1.0.0"

    # API Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8002

    # Model Settings
    MODEL_NAME: str = Field(
        default="sshleifer/distilbart-cnn-12-6",
        description="Hugging Face model name for summarization",
    )

    # Performance Settings
    MAX_CHUNK_SIZE: int = Field(default=800, ge=100, le=1000)
    CHUNK_OVERLAP: int = Field(default=100, ge=0, le=200)
    MAX_QUEUE_SIZE: int = Field(default=10, ge=1, le=50)

    # Cache Settings
    REDIS_URL: str = "redis://localhost:6379"
    CACHE_TTL: int = 3600  # 1 hour

    class Config:
        env_file = ".env"


settings = Settings()
