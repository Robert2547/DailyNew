"""
Debug demo script for testing Financial News Scraper API
Includes detailed logging and error tracking
"""
import requests
import json
from datetime import datetime
from typing import Optional, Dict, Any
import time
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
logger.debug("Loading environment variables")

class FinancialNewsAPIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        logger.debug(f"Initializing API client with base URL: {base_url}")
        self.base_url = base_url
        self.api_key = os.getenv("SCRAPEOPS_API_KEY")
        
        if not self.api_key:
            logger.error("SCRAPEOPS_API_KEY not found in environment variables")
            raise ValueError("SCRAPEOPS_API_KEY not found in environment variables")
            
        logger.debug(f"API Key found: {self.api_key[:5]}...")
        self.headers = {
            "X-API-Key": self.api_key,
            "Accept": "application/json"
        }

    def get_news(self, ticker: str) -> Optional[Dict[str, Any]]:
        """Fetch news for a given ticker symbol with detailed error logging"""
        url = f"{self.base_url}/api/v1/news/{ticker}"
        logger.info(f"Making request to: {url}")
        logger.debug(f"Headers: {self.headers}")
        
        try:
            logger.debug("Sending GET request...")
            response = requests.get(url, headers=self.headers)
            logger.debug(f"Response status code: {response.status_code}")
            logger.debug(f"Response headers: {response.headers}")
            
            # Log the raw response for debugging
            try:
                logger.debug(f"Response content: {response.text[:500]}...")
            except Exception as e:
                logger.debug(f"Could not log response content: {e}")
            
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.HTTPError as http_err:
            logger.error(f"HTTP error occurred: {http_err}")
            logger.error(f"Response content: {response.text}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Error making request: {e}")
            return None
        except json.JSONDecodeError as json_err:
            logger.error(f"Error decoding JSON response: {json_err}")
            logger.error(f"Raw response: {response.text}")
            return None

def test_single_ticker(ticker: str = "AAPL"):
    """
    Test the API with a single ticker with detailed debugging
    """
    logger.info(f"Starting single ticker test for {ticker}")
    
    try:
        # Initialize client
        logger.debug("Initializing API client...")
        client = FinancialNewsAPIClient()
        
        # Fetch news
        logger.info(f"Fetching news for {ticker}")
        start_time = time.time()
        
        news_data = client.get_news(ticker)
        end_time = time.time()
        
        if news_data:
            logger.info(f"Successfully retrieved news for {ticker}")
            logger.debug(f"News data: {json.dumps(news_data, indent=2)}")
            print_news_data(news_data)
        else:
            logger.error(f"No news data received for {ticker}")
            
        logger.info(f"Time taken: {end_time - start_time:.2f} seconds")
        
    except Exception as e:
        logger.exception(f"Unexpected error during test: {e}")

def print_news_data(news_data: Dict[str, Any]) -> None:
    """Pretty print the news data"""
    try:
        print("\n" + "="*80)
        print(f"📰 News for {news_data['ticker']} | Retrieved at: {news_data.get('timestamp', 'N/A')}")
        print("="*80)
        
        articles = news_data.get('articles', [])
        if not articles:
            logger.warning("No articles found in news data")
            print("\nNo articles found.")
            return
            
        for idx, article in enumerate(articles, 1):
            print(f"\n📌 Article {idx}:")
            print(f"Title: {article.get('title', 'N/A')}")
            print(f"Source: {article.get('source', 'N/A')}")
            print(f"Date: {article.get('date', 'N/A')}")
            print(f"URL: {article.get('url', 'N/A')}")
            print("-"*80)
            
    except Exception as e:
        logger.exception(f"Error printing news data: {e}")

def main():
    """Main function with basic error handling"""
    logger.info("Starting debug demo")
    
    try:
        # Check if the API is running
        logger.debug("Checking API status...")
        health_check = requests.get("http://localhost:8000/docs")
        if health_check.status_code != 200:
            logger.error("API appears to be down. Please ensure it's running.")
            return
            
        logger.info("API is running, proceeding with test")
        
        # Run single ticker test
        test_single_ticker("AAPL")
        
    except requests.exceptions.ConnectionError:
        logger.error("Could not connect to the API. Is it running?")
    except Exception as e:
        logger.exception(f"Unexpected error in main: {e}")

if __name__ == "__main__":
    main()