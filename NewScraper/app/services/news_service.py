"""
News service implementation
"""
from fastapi import BackgroundTasks
from app.models.schemas import NewsResponse, NewsArticle
from app.services.cache import CacheService
from app.scrapers import YahooScraper, ReutersScraper
from app.config.source_configs import SOURCES
from typing import List
import logging
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

class NewsService:
    def __init__(self):
        self.cache_service = CacheService()
        """ NEED TO ADD MORE SCRAPERS HERE """
        self.scrapers = [
            (YahooScraper(SOURCES["yahooFinance"]), "Yahoo Finance"),
            (ReutersScraper(SOURCES["reuters"]), "Reuters"),
        ]

    async def get_news(self, ticker: str, background_tasks: BackgroundTasks) -> NewsResponse:
        """Get news for a ticker from cache or scrape it"""
        # Check cache first
        cached_news = await self.cache_service.get_news(ticker)
        if cached_news:
            return NewsResponse(
                ticker=ticker,
                articles=cached_news,
                status="success",
                message="Retrieved from cache"
            )

        # Scrape news if not in cache
        articles = await self._scrape_all_sources(ticker)
        
        # Cache results in background
        background_tasks.add_task(self.cache_service.set_news, ticker, articles)
        
        return NewsResponse(
            ticker=ticker,
            articles=articles,
            status="success"
        )

    async def _scrape_all_sources(self, ticker: str) -> List[NewsArticle]:
        """Scrape news from all sources in parallel"""
        articles = []
        
        def scrape_source(scraper, source_name):
            try:
                if source_name == "Reuters":
                    news = scraper.fetch_and_extract_article_api(ticker)
                else:
                    news = scraper.get_news_content(ticker)
                    
                if news:
                    return [
                        NewsArticle(
                            title=title,
                            url=url,
                            date=date,
                            source=source_name
                        )
                        for title, url, date in zip(
                            news["titles"], news["urls"], news["dates"]
                        )
                    ]
            except Exception as e:
                logger.error(f"Error scraping {source_name}: {str(e)}")
                return []

        with ThreadPoolExecutor(max_workers=len(self.scrapers)) as executor:
            results = list(executor.map(
                lambda x: scrape_source(*x), 
                self.scrapers
            ))
            
        # Flatten results
        for result in results:
            articles.extend(result or [])
            
        return articles