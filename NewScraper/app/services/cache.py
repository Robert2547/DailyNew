"""
Cache service implementation
"""
from typing import List, Optional
from app.models.schemas import NewsArticle
from app.core.config import settings
import json
import logging

logger = logging.getLogger(__name__)

class CacheService:
    def __init__(self):
        self.use_cache = settings.USE_REDIS
        if self.use_cache:
            try:
                import redis
                self.redis_client = redis.Redis(
                    host=settings.REDIS_HOST,
                    port=settings.REDIS_PORT,
                    db=0
                )
                logger.debug("Redis cache initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Redis: {e}")
                self.use_cache = False

    async def get_news(self, ticker: str) -> Optional[List[NewsArticle]]:
        """Get cached news for a ticker"""
        if not self.use_cache:
            return None
            
        try:
            cache_key = f"news:{ticker}"
            cached = self.redis_client.get(cache_key)
            if cached:
                return [NewsArticle(**article) for article in json.loads(cached)]
            return None
        except Exception as e:
            logger.error(f"Error getting cached news: {e}")
            return None

    async def set_news(self, ticker: str, articles: List[NewsArticle]):
        """Cache news for a ticker"""
        if not self.use_cache:
            return
            
        try:
            cache_key = f"news:{ticker}"
            articles_json = json.dumps([article.dict() for article in articles])
            self.redis_client.setex(
                cache_key,
                settings.CACHE_EXPIRATION,
                articles_json
            )
            logger.debug(f"Cached {len(articles)} articles for {ticker}")
        except Exception as e:
            logger.error(f"Error caching news: {e}")