from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.base import Base, engine
from app.api import router as api_router
from app.services import router as services_router

app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include the router
app.include_router(api_router)
app.include_router(services_router)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=settings.HOST, port=settings.PORT)
