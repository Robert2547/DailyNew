"""
News endpoints implementation
"""
from fastapi import APIRouter, Depends, BackgroundTasks, Response
from app.models.schemas import NewsResponse, ErrorResponse
from app.services.news_service import NewsService
from app.api.dependencies import verify_api_key
from app.core.exceptions import NewsScrapingException
from typing import List

router = APIRouter(prefix="/news", tags=["news"])

@router.get("/{ticker}", response_model=NewsResponse)
async def get_news(
    ticker: str,
    response: Response,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(verify_api_key),
    news_service: NewsService = Depends()
):
    """Get financial news for a specific ticker"""
    try:
        return await news_service.get_news(ticker, background_tasks)
    except NewsScrapingException as e:
        raise e