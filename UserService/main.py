# main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.endpoints import profiles
from contextlib import asynccontextmanager
from app.db.base import Base, init_db
import logging
from app.core.config import settings
import os

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        # Force test settings
        if os.getenv("TESTING", "").lower() == "true":
            logger.info("Using test database configuration...")
            os.environ.update({
                "DB_USER": "test_user",
                "DB_PASSWORD": "test_password",
                "USER_DB_PORT": "5437",
                "USER_DB_NAME": "user_test_db"
            })
            
        # Initialize database and get engine
        engine = init_db()
        # Create tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise
    yield
    logger.info("Shutting down application...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(profiles.router, prefix="/api/v1/profiles", tags=["profiles"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)