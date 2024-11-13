"""
News endpoint routes
"""
from fastapi import APIRouter, Depends, BackgroundTasks
from app.api.dependencies import verify_api_key
from app.services.news_service import NewsService
from app.models.schemas import NewsResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/news", tags=["news"])

# Initialize NewsService outside the route
news_service = NewsService()

@router.get("/{ticker}", response_model=NewsResponse)
async def get_news(
    ticker: str,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(verify_api_key)
):
    """
    Get financial news for a specific ticker
    
    Args:
        ticker: Stock ticker symbol
        background_tasks: FastAPI background tasks
        api_key: API key for authentication
    
    Returns:
        NewsResponse: News data with articles from all sources
    """
    try:
        logger.debug(f"Received request for ticker: {ticker}")
        return await news_service.get_news(ticker, background_tasks)
    except Exception as e:
        logger.exception(f"Error processing request for {ticker}: {str(e)}")
        raise