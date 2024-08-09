from .auth import router as auth_router
from .summarize import router  as endpoint_router
from fastapi import APIRouter
from .api import router as api_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(endpoint_router, tags=["endpoints"])
router.include_router(api_router, tags=["api"])

__all__ = ["router"]
