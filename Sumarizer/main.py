from fastapi import FastAPI
from app.core.config import settings
from Sumarizer.app.api.v1.endpoints import summarizer
import uvicorn

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

app.include_router(
    summarizer.router,
    prefix="/api/v1",
    tags=["summarizer"]
)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
