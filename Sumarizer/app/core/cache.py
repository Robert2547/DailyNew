import redis
import json
import hashlib
from app.core.config import settings

class CacheManager:
    def __init__(self):
        self.redis = redis.from_url(settings.REDIS_URL)
        
    def get_cache_key(self, content: str) -> str:
        """Generate cache key from content."""
        return hashlib.md5(content.encode()).hexdigest()
        
    async def get_summary(self, content: str) -> str | None:
        """Get cached summary."""
        key = self.get_cache_key(content)
        cached = self.redis.get(key)
        return cached.decode() if cached else None
        
    async def set_summary(self, content: str, summary: str):
        """Cache summary with TTL."""
        key = self.get_cache_key(content)
        self.redis.setex(key, settings.CACHE_TTL, summary)
