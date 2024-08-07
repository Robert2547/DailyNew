#app/__init__.py
from fastapi import FastAPI



app = FastAPI()

from .api import router

# Include the router
app.include_router(router)

# Import these at the end to avoid circular imports
from .utils import helpers
