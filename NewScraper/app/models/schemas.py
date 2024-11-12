"""
Pydantic models for request/response schemas
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class NewsArticle(BaseModel):
    """Model for a single news article"""
    title: str
    url: str
    date: str
    source: str
    paragraphs: Optional[str] = ""

class NewsResponse(BaseModel):
    """Model for the API response"""
    ticker: str
    timestamp: datetime = Field(default_factory=datetime.now)
    articles: List[NewsArticle]
    status: str
    message: Optional[str] = None

class ErrorResponse(BaseModel):
    """Model for error responses"""
    status: str = "error"
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)