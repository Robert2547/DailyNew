import os
from pathlib import Path
from utils import save_to_json, timing
from config import SCRAPEOPS_API_KEY
from scrapers import YahooScraper, ReutersScraper


@timing
def main():
    # URL = "https://www.reuters.com/markets/companies/AVGO.O/profile"
    URL = "https://finance.yahoo.com/quote/AVGO/"
    # scraper = ReutersScraper(SCRAPEOPS_API_KEY)
    scraper = YahooScraper(SCRAPEOPS_API_KEY)

    news_content = scraper.get_news_content(URL)
    print("news_content: ", news_content["titles"])
    # Save the results
    output_folder = Path("output")
    output_file = output_folder / "yahoo_articles.json"

    # Assuming news_content is defined earlier in your code
    save_to_json(news_content, output_file)

if __name__ == "__main__":
    main()
