from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.core.config import settings
import uvicorn
from app.api.v1 import auth

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)