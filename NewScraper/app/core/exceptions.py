"""
Custom exceptions and exception handlers for the API
"""
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from datetime import datetime

class NewsScrapingException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

async def news_exception_handler(request: Request, exc: NewsScrapingException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "message": exc.message,
            "timestamp": datetime.now().isoformat()
        }
    )

def configure_exception_handlers(app: FastAPI):
    app.add_exception_handler(NewsScrapingException, news_exception_handler)