"""
Main FastAPI application entry point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import Settings
from app.api.routes import news
from app.core.exceptions import configure_exception_handlers
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def create_app(settings: Settings) -> FastAPI:
    """Create and configure FastAPI application"""
    logger.info("Initializing FastAPI application")

    app = FastAPI(
        title=settings.APP_NAME,
        description=settings.APP_DESCRIPTION,
        version=settings.APP_VERSION,
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ALLOWED_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(news.router, prefix="/api/v1")

    # Configure exception handlers
    configure_exception_handlers(app)

    logger.info("FastAPI application configured successfully")
    return app


app = create_app(Settings())


@app.on_event("startup")
async def startup_event():
    logger.info("Application starting up...")
    # Add any startup tasks here


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Application shutting down...")
    # Add any cleanup tasks here
