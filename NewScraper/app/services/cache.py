"""
Redis cache service implementation
"""
import redis
from typing import Optional, List
from app.models.schemas import NewsArticle
from app.core.config import Settings

import json

class CacheService:
    def __init__(self):
        self.settings = Settings()
        self.redis_client = redis.Redis(
            host=self.settings.REDIS_HOST,
            port=self.settings.REDIS_PORT,
            db=0
        )
        self.cache_expiration = self.settings.CACHE_EXPIRATION

    async def get_news(self, ticker: str) -> Optional[List[NewsArticle]]:
        """Get cached news for a ticker"""
        cache_key = f"news:{ticker}"
        cached = self.redis_client.get(cache_key)
        if cached:
            return [NewsArticle(**article) for article in json.loads(cached)]
        return None

    async def set_news(self, ticker: str, articles: List[NewsArticle]):
        """Cache news for a ticker"""
        cache_key = f"news:{ticker}"
        articles_json = json.dumps([article.dict() for article in articles])
        self.redis_client.setex(
            cache_key,
            self.cache_expiration,
            articles_json
        )