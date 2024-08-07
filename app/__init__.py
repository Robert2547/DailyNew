from fastapi import FastAPI

from .services import article, summarizer

app = FastAPI()

# Import these after creating the app instance
from .api.endpoints import router

# Include the router
app.include_router(router)

# Import these at the end to avoid circular imports
from .utils import helpers
