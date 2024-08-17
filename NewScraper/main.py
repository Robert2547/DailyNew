import os
from pathlib import Path
from utils import save_to_json, timing
from config import SCRAPEOPS_API_KEY
from scrapers import YahooScraper, ReutersScraper, MarketWatchScraper
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from config import SOURCES, HEADERS
import requests
from bs4 import BeautifulSoup


@timing
def main():
    ticker = "AAPL"  # Example ticker

    # TODO: Implement parallel scraping using threads or asyncio

    # Initialize scrapers
    # yahoo_scraper = YahooScraper(SOURCES["yahooFinance"])
    # marketwatch_scraper = MarketWatchScraper(SOURCES["marketWatch"])
    # reuters_scraper = ReutersScraper(SOURCES["reuters"])


    # Get news content
    # yahoo_news = yahoo_scraper.get_news_content(ticker)
    # marketwatch_news = marketwatch_scraper.get_news_content(ticker)
    # reuters_news = reuters_scraper.fetch_and_extract_article_ap(ticker)

    
    # Process the news content as needed
    # print("Yahoo Finance News:")
    # for title, url, date in zip(yahoo_news["titles"], yahoo_news["urls"], yahoo_news["dates"]):
    #     print(f"Title: {title}")
    #     print(f"Datetime: {date}")
    #     print("---")

    # print("\n\nMarketWatch News:")
    # for title, url, date in zip(marketwatch_news["titles"], marketwatch_news["urls"], marketwatch_news["dates"]):
    #     print(f"Title: {title}")
    #     print("---")

    # print("\n\nReuters News:")
    # for title, url, date in zip(reuters_news["titles"], reuters_news["urls"], reuters_news["dates"]):
    #     print(f"Title: {title}")
    #     print(f"Date: {date}")
    #     print("---")
    

if __name__ == "__main__":
    main()
