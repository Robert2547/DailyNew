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
    
    # Save the results
    output_folder = Path("output")
    output_folder.mkdir(exist_ok=True)
    output_file = output_folder / "yahoo_articles.json"
    save_to_json(news_content, output_file)

    print(f"Processed {len(news_content['titles'])} articles. Results saved to {output_file}")

if __name__ == "__main__":
    main()