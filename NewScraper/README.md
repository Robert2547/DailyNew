# Financial News Scraper API

A FastAPI-based microservice for scraping financial news from multiple sources including Yahoo Finance, Reuters, and etc... The service provides a RESTful API interface for retrieving news articles based on stock tickers.

## Features

- Multi-source news scraping
- Parallel processing of news sources
- API key authentication
- Rate limiting
- Error handling
- CORS support
- Logging
- Documentation via Swagger UI and ReDoc

## Tech Stack

- Python 3.8+
- FastAPI
- BeautifulSoup4
- Newspaper3k
- Redis (for caching)
- Pydantic
- Uvicorn

## Project Structure

```
financial_news_service/
├── app/
│   ├── api/                    # API routes and dependencies
│   ├── core/                   # Core configuration and settings
│   ├── models/                 # Pydantic models
│   ├── services/              # Business logic
│   ├── config/                # Source configurations
│   ├── scrapers/              # News scrapers
│   └── utils/                 # Utility functions
├── .env                       # Environment variables
├── main.py                    # Application entry point
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation
```

## Installation

1. Clone the repository:
```bash
git clone 
cd financial-news-service
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory:
```env
SCRAPEOPS_API_KEY=your_api_key_here
```

## Running the Application

1. Start the server:
```bash
# Option 1: Using the entry point
python main.py

# Option 2: Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Usage

### Get News for a Ticker

```python
import requests

def get_news(ticker: str):
    response = requests.get(
        f"http://localhost:8000/api/v1/news/{ticker}",
        headers={"X-API-Key": "your_api_key_here"}
    )
    return response.json()

# Example usage
news = get_news("AAPL")
print(news)
```

### Example Response

```json
{
    "ticker": "AAPL",
    "timestamp": "2024-11-12T10:30:00",
    "articles": [
        {
            "title": "Apple to Launch Smart Home Camera in 2026",
            "url": "https://finance.yahoo.com/news/apple-launch-smart-home...",
            "date": "2024-11-12 10:15:00",
            "source": "Yahoo Finance",
            "paragraphs": "Article content here..."
        }
    ],
    "status": "success"
}
```

## Demo Script

Here's a complete demo script to test the API:

```python
import requests
import json
from typing import Optional
from datetime import datetime

class NewsAPIClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.headers = {"X-API-Key": api_key}

    def get_news(self, ticker: str) -> Optional[dict]:
        """Fetch news for a given ticker"""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/news/{ticker}",
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching news: {e}")
            return None

def print_news(news_data: dict):
    """Pretty print news data"""
    if not news_data:
        print("No news data available")
        return

    print("\n" + "="*50)
    print(f"News for {news_data['ticker']} at {news_data['timestamp']}")
    print("="*50)

    for article in news_data['articles']:
        print(f"\nTitle: {article['title']}")
        print(f"Source: {article['source']}")
        print(f"Date: {article['date']}")
        print(f"URL: {article['url']}")
        print("-"*50)

def main():
    # Initialize client
    client = NewsAPIClient(
        base_url="http://localhost:8000",
        api_key="your_api_key_here"
    )

    # Test with different tickers
    tickers = ["AAPL", "MSFT", "GOOGL"]
    
    for ticker in tickers:
        print(f"\nFetching news for {ticker}...")
        news = client.get_news(ticker)
        print_news(news)
        print("\n")

if __name__ == "__main__":
    main()
```

Save this as `demo.py` and run:
```bash
python demo.py
```

## Development

### Adding a New News Source

1. Create a new scraper in `app/scrapers/`:
```python
from app.scrapers.base import BaseScraper

class NewSourceScraper(BaseScraper):
    def __init__(self, config, use_headers=True):
        super().__init__(config, use_headers)
    
    def extract_news_content(self, soup, main_url):
        # Implementation here
        pass
```

2. Add source configuration in `app/config/source_configs.py`:
```python
SOURCES = {
    "newSource": {
        "base_url": "https://example.com/stocks/{ticker}",
        "headers": HEADERS,
        "company": {
            "titles": "css_selector_for_titles",
            "urls": "css_selector_for_urls",
            "dates": "css_selector_for_dates",
        }
    }
}
```

3. Register the scraper in `app/services/news_service.py`:
```python
self.scrapers = [
    (NewSourceScraper(SOURCES["newSource"]), "New Source"),
    # ... other scrapers
]
```