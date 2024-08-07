from .auth import router as auth_router
from .endpoints import router  as endpoint_router
from fastapi import APIRouter

router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(endpoint_router, tags=["endpoints"])
__all__ = ["router"]
