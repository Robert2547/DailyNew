"""
Centralized logging configuration
"""
import logging
from rich.logging import RichHandler

def setup_logging():
    # Remove any existing handlers
    logging.getLogger().handlers = []
    
    # Configure basic logging
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            RichHandler(rich_tracebacks=True)
        ]
    )
    
    # Set levels for specific loggers
    logging.getLogger("app.scrapers").setLevel(logging.DEBUG)
    logging.getLogger("app.services").setLevel(logging.DEBUG)
    logging.getLogger("app.utils").setLevel(logging.DEBUG)
    
    # Create logger for this module
    logger = logging.getLogger(__name__)
    logger.debug("Logging configured")