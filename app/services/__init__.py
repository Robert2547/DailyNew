"""
This package provides functionality for article content extraction, summarization, and user authentication.
"""

from .article import get_content, fetch_article_content, extract_article_content
from .summarizer import load_model, summarize_content
from .auth import (
    get_user,
    create_user,
    authenticate_user,
    verify_token,
    get_current_user,
    create_password_reset_token,
    reset_password,
    create_access_token, create_token
)
from .test import router as test_router
from fastapi import APIRouter

router = APIRouter()
router.include_router(test_router, tags=["Test"])

__all__ = [
    "router",
    # Article module
    "get_content",
    "fetch_article_content",
    "extract_article_content",
    # Summarizer module
    "load_model",
    "summarize_content",
    # Auth module
    "get_user",
    "create_user",
    "authenticate_user",
    "verify_token",
    "get_current_user",
    "create_password_reset_token",
    "reset_password",
    "create_access_token", "create_token"
]
