# Financial News Scraper API

A FastAPI-based microservice for parallel scraping of financial news from multiple sources including Yahoo Finance, Reuters, and more. The service provides a RESTful API interface for retrieving recent news articles based on stock tickers.

## Features

- **Multi-Source News Aggregation**
  - Yahoo Finance integration
  - Reuters integration
  - Easily extensible for additional sources

- **Performance Optimizations**
  - Parallel scraping of multiple sources
  - Redis caching support
  - Efficient data processing

- **API Features**
  - RESTful endpoints
  - API key authentication
  - Rate limiting
  - CORS support
  - Comprehensive error handling

- **Developer Features**
  - Interactive API documentation (Swagger UI)
  - Detailed logging
  - Type hints throughout
  - Modular architecture

## Tech Stack

- **Core Framework**
  - Python 3.9+
  - FastAPI
  - Pydantic
  - Uvicorn

- **Scraping & Processing**
  - BeautifulSoup4
  - Newspaper3k
  - LXML

- **Caching & Performance**
  - Redis
  - ThreadPoolExecutor

- **Development & Testing**
  - Rich (for CLI interface)
  - Python-dotenv
  - Pytest (for testing)

## Project Structure

```plaintext
financial_news_service/
├── app/
│   ├── api/                    # API implementation
│   │   ├── routes/            # API endpoints
│   │   └── dependencies.py    # API dependencies
│   ├── core/                  # Core functionality
│   │   ├── config.py         # Configuration settings
│   │   └── exceptions.py     # Custom exceptions
│   ├── models/               # Data models
│   │   └── schemas.py        # Pydantic schemas
│   ├── services/             # Business logic
│   │   ├── news_service.py  # News aggregation service
│   │   └── cache.py         # Caching service
│   ├── scrapers/             # News scrapers
│   │   ├── base.py          # Base scraper class
│   │   ├── yahoo.py         # Yahoo Finance scraper
│   │   └── reuters.py       # Reuters scraper
│   └── utils/                # Utility functions
├── .env                      # Environment variables
├── .gitignore               # Git ignore rules
├── main.py                  # Application entry point
├── requirements.txt         # Project dependencies
└── README.md               # Documentation
```

## Installation

1. **Clone the Repository**
```bash
git clone <repository-url>
cd financial-news-service
```

2. **Set Up Virtual Environment**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure Environment**
Create `.env` file in the root directory:
```env
# Required
SCRAPEOPS_API_KEY=your_api_key_here

# Optional - Redis configuration
USE_REDIS=False
REDIS_HOST=localhost
REDIS_PORT=6379
```

## Running the Application

1. **Start the Server**
```bash
# Using uvicorn (recommended for development)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or using the entry point
python main.py
```

## API Usage

### Basic Usage

```python
import requests

class NewsClient:
    def __init__(self, api_key: str, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.headers = {"X-API-Key": api_key}

    def get_news(self, ticker: str) -> dict:
        response = requests.get(
            f"{self.base_url}/api/v1/news/{ticker}",
            headers=self.headers
        )
        return response.json()

# Example usage
client = NewsClient(api_key="your_api_key_here")
news = client.get_news("AAPL")
```

### Response Format

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

## Testing

### Running the Demo Script

The project includes a comprehensive demo script with features like:
- Interactive menu
- Multiple ticker testing
- System health checks
- Performance metrics

```bash
# Run the demo script
python demo.py
```

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=app tests/
```

## Development

### Adding a New News Source

1. **Create Scraper Class**
```python
# app/scrapers/new_source.py
from app.scrapers.base import BaseScraper

class NewSourceScraper(BaseScraper):
    def __init__(self, config, use_headers=True):
        super().__init__(config, use_headers)
    
    def extract_news_content(self, soup, main_url):
        # Implementation here
        pass
```

2. **Add Configuration**
```python
# app/config/source_configs.py
SOURCES = {
    "new_source": {
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

3. **Register Scraper**
```python
# app/services/news_service.py
self.scrapers = [
    (NewSourceScraper(SOURCES["new_source"]), "New Source"),
    # ... other scrapers
]
```
