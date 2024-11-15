"""Logging middleware for request tracking."""

from fastapi import Request
import time
import logging
from typing import Callable
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self, request: Request, call_next: Callable
    ):
        """Log request and response details."""
        start_time = time.time()
        
        # Log request
        logger.info(
            f"Request: {request.method} {request.url.path}"
            f" Client: {request.client.host if request.client else 'Unknown'}"
        )
        
        response = await call_next(request)
        
        # Log response
        process_time = time.time() - start_time
        logger.info(
            f"Response: {response.status_code}"
            f" Process Time: {process_time:.3f}s"
        )
        
        return response
