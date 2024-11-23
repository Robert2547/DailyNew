from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.core.config import settings
import uvicorn
from app.api.v1.endpoint import auth, system
from app.db.base import Base, engine
from contextlib import asynccontextmanager
import logging
import os

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables
    if os.getenv("TESTING", "false").lower() == "true":
        # Skip table creation in test mode
        logger.info("Test mode: Skipping table creation in main.py")
        yield
    else:
        # Production mode: Create tables
        logger.info("Creating database tables...")
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating database tables: {e}")
            raise e
        yield
        
    # Shutdown: Add cleanup if needed
    logger.info("Shutting down application...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(system.router, prefix=f"{settings.API_V1_STR}/system", tags=["system"])

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)