import os
from dotenv import load_dotenv

load_dotenv()

SCRAPEOPS_API_KEY = os.getenv("SCRAPEOPS_API_KEY")
if not SCRAPEOPS_API_KEY:
    raise ValueError("SCRAPEOPS_API_KEY not found in environment variables")

PROXY_URL = "https://proxy.scrapeops.io/v1/"
