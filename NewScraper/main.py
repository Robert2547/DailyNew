import os
from pathlib import Path
import concurrent.futures
from utils import save_to_json, timing
import json, cProfile
import time
from config import SCRAPEOPS_API_KEY
import pstats
from io import StringIO
from scrapers import YahooScraper, ReutersScraper


@timing
def main():

    # TODO: Make URL dynamic
    # URL = "https://www.reuters.com/markets/companies/AAPL.O/profile"
    URL = "https://finance.yahoo.com/quote/AVGO/"
    # scraper = ReutersScraper(SCRAPEOPS_API_KEY)
    scraper = YahooScraper(SCRAPEOPS_API_KEY)

    news_content = scraper.get_news_content(URL)

    def article_generator():
        for title, url, date in zip(
            news_content["titles"], news_content["urls"], news_content["dates"]
        ):
            yield url

    output_folder = Path("output")
    output_folder.mkdir(exist_ok=True)
    output_file = output_folder / "articles.json"
    articles = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_url = {
            executor.submit(scraper.fetch_and_extract_article, url): url
            for url in article_generator()
        }

        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                article_details = future.result()
                articles.append(article_details)
            except Exception as exc:
                print(f"{url} generated an exception: {exc}")
    save_to_json(articles, output_file)


if __name__ == "__main__":

    main()
