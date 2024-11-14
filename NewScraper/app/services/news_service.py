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
from concurrent.futures import ThreadPoolExecutor, as_completed

logger = logging.getLogger(__name__)

class NewsService:
    def __init__(self):
        """Initialize NewsService with scrapers and optional cache service"""
        try:
            logger.debug("Initializing NewsService")
            
            # Initialize cache service
            try:
                self.cache_service = CacheService()
                logger.debug("Cache service initialized")
            except Exception as cache_error:
                logger.warning(f"Cache service not available: {cache_error}")
                self.cache_service = None
            
            # Initialize scrapers
            self.scrapers = [
                (YahooScraper(SOURCES["yahooFinance"]), "Yahoo Finance"),
                (ReutersScraper(SOURCES["reuters"]), "Reuters"),
            ]
            logger.debug(f"Initialized {len(self.scrapers)} scrapers")
            
        except Exception as e:
            logger.exception("Error initializing NewsService")
            raise

    async def get_news(self, ticker: str, background_tasks: BackgroundTasks) -> NewsResponse:
        """Get news for a ticker from cache or scrape it"""
        try:
            logger.debug(f"Getting news for ticker: {ticker}")
            
            # Check cache if available
            if self.cache_service and self.cache_service.use_cache:
                cached_news = await self.cache_service.get_news(ticker)
                if cached_news:
                    logger.debug(f"Cache hit for ticker {ticker}")
                    return NewsResponse(
                        ticker=ticker,
                        articles=cached_news,
                        status="success",
                        message="Retrieved from cache"
                    )

            # Scrape news if not in cache
            logger.debug(f"Scraping fresh news for {ticker}")
            articles = await self._scrape_all_sources(ticker)
            
            # Cache results in background if cache service is available
            if self.cache_service and self.cache_service.use_cache:
                logger.debug(f"Scheduling cache update for {ticker}")
                background_tasks.add_task(self.cache_service.set_news, ticker, articles)
            
            return NewsResponse(
                ticker=ticker,
                articles=articles,
                status="success"
            )
            
        except Exception as e:
            logger.exception(f"Error getting news for {ticker}")
            raise

    async def _scrape_all_sources(self, ticker: str) -> List[NewsArticle]:
        """Scrape news from all sources in parallel"""
        articles = []
        
        def scrape_source(scraper, source_name):
            """Helper function to scrape a single source"""
            try:
                logger.debug(f"Scraping {source_name} for {ticker}")
                
                if source_name == "Reuters":
                    logger.debug(f"Using API method for {source_name}")
                    news = scraper.fetch_and_extract_article_api(ticker)
                    print("\nLENGTH OF REUTERS: ", len(news["titles"]))
                else:
                    logger.debug(f"Using standard method for {source_name}")
                    news = scraper.get_news_content(ticker)
                    print("\nLENGTH OF YAHOO: ", len(news["titles"]))
                
                if news and news.get("titles"):
                    source_articles = [
                        NewsArticle(
                            title=title,
                            url=url,
                            date=date,
                            source=source_name,
                            paragraphs=paragraph if paragraph else ""
                        )
                        for title, url, date, paragraph in zip(
                            news["titles"],
                            news["urls"],
                            news["dates"],
                            news.get("paragraphs", [""] * len(news["titles"]))
                        )
                    ]
                    logger.debug(f"Found {len(source_articles)} articles from {source_name}")
                    return source_articles
                else:
                    logger.warning(f"No news found from {source_name}")
                    return []
                    
            except Exception as e:
                logger.exception(f"Error scraping {source_name}: {str(e)}")
                return []

        # Use ThreadPoolExecutor for parallel scraping
        with ThreadPoolExecutor(max_workers=len(self.scrapers)) as executor:
            logger.debug(f"Starting parallel execution with {len(self.scrapers)} scrapers")
            
            # Create futures dictionary
            future_to_scraper = {
                executor.submit(scrape_source, scraper, name): (scraper, name)
                for scraper, name in self.scrapers
            }
            
            # Process completed futures
            for future in as_completed(future_to_scraper):
                scraper_info = future_to_scraper[future]
                try:
                    result = future.result()
                    if result:
                        logger.debug(f"Adding {len(result)} articles from {scraper_info[1]}")
                        articles.extend(result)
                except Exception as e:
                    logger.error(f"Error processing results from {scraper_info[1]}: {str(e)}")
        
        logger.debug(f"Total articles collected: {len(articles)}")
        return articles

    def _format_article(self, title: str, url: str, date: str, source: str, paragraph: str = "") -> NewsArticle:
        """Helper method to format article data"""
        return NewsArticle(
            title=title,
            url=url,
            date=date,
            source=source,
            paragraphs=paragraph
        )