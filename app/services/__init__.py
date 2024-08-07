"""
This package provides functionality for article content extraction, summarization, and user authentication.
"""

from .article import get_content, fetch_article_content, extract_article_content
from .summarizer import load_model, summarize_content
from .auth import get_user, create_user, authenticate_user

__all__ = [
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
]