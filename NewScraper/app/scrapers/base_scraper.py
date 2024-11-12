from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from utils import timing, get_proxy_response
import concurrent.futures
from newspaper import Article
from datetime import datetime
import requests
from app.core.config import settings  # Import settings instance


class BaseScraper(ABC):
    def __init__(self, config, use_headers=True):
        self.config = config
        self.base_url = config.get("base_url", "")
        self.headers = config.get("headers", {}) if use_headers else {}
        self.api_key = settings.SCRAPEOPS_API_KEY

    def parse_html(self, content):
        return BeautifulSoup(content, "html.parser")

    @abstractmethod
    def extract_news_content(self, soup, main_url):
        pass

    def extract_article_details(self, url):
        article = Article(url)
        article.download()
        article.parse()
        return article.text

    @abstractmethod
    def get_url(self, ticker):
        pass

    def is_recent_article(self, date_string):
        try:
            article_date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
            return (datetime.now() - article_date).days < 1
        except ValueError:
            print(f"Unable to parse date: {date_string}")
            return False

    def standardize_date(self, date_string):
        # TODO: Implement date standardization logic here
        # Convert various date formats to "YYYY-MM-DD HH:MM:SS"
        pass

    @timing
    def get_news_content(self, ticker):
        url = self.get_url(ticker)
        response = requests.get(url, headers=self.headers)
        # TODO: Fix 401 error for marketplace
        if response.status_code != 200:
            print(f"Failed to fetch URL: {response.content}")
            raise Exception(f"Request failed with status code: {response.status_code}")
        soup = self.parse_html(response.content)
        try:
            news_content = self.extract_news_content(soup, url)
            self.fetch_article_contents(news_content)
            return news_content
        except Exception as e:
            print(f"Error extracting news content: {e}")
            return {"titles": [], "urls": [], "dates": [], "paragraphs": []}

    # Fetches the article content for each URL in the news_content dictionary, use Newspaper3k for scraping
    def fetch_article_contents(self, news_content):
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {
                executor.submit(self.extract_article_details, article_url): article_url
                for article_url in news_content["urls"]
            }

            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    article_text = future.result()
                    index = news_content["urls"].index(url)
                    news_content["paragraphs"][index] = article_text
                except Exception as exc:
                    print(f"Error fetching article content: {exc}")
                    continue

    # Same as fetch_article_contents but uses the SCRAPEOPS API, instead of Newspaper3k
    def fetch_article_contents_api(self, news_content):
        try:

            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                future_to_url = {
                    executor.submit(
                        self.fetch_and_extract_single_article, article_url
                    ): article_url
                    for article_url in news_content["urls"]
                }

                for future in concurrent.futures.as_completed(future_to_url):
                    url = future_to_url[future]
                    try:
                        article_text = future.result()
                        index = news_content["urls"].index(url)
                        news_content["paragraphs"][index] = article_text
                    except Exception as exc:
                        print(f"{url} generated an exception: {exc}")
                        news_content["paragraphs"][
                            index
                        ] = ""  # Set empty string for failed fetches

            return news_content
        except Exception as e:
            print(f"Error in fetch_article_contents_api: {e}")
            return {"titles": [], "urls": [], "dates": [], "paragraphs": []}

    # Fetches and extracts the article content for a single URL using the SCRAPEOPS API
    def fetch_and_extract_single_article(self, url):
        try:
            response = get_proxy_response(url, self.api_key)
            if response.status_code != 200:
                raise Exception(f"Failed to fetch URL: {url}")

            soup = self.parse_html(response.text)
            article_details = self.extract_article_details(soup)
            paragraphs = article_details.get("paragraphs", "")
            return paragraphs
        except Exception as e:
            print(f"Error fetching and extracting single article content: {e}")
            return ""

    @timing
    def fetch_and_extract_article_api(self, ticker):
        try:
            url = self.get_url(ticker)
            response = get_proxy_response(url, self.api_key)
            if response.status_code != 200:
                raise Exception(f"Failed to fetch URL: {url}")
            soup = self.parse_html(response.content)
            news_content = self.extract_news_content(soup, url)
            return self.fetch_article_contents_api(news_content)
        except Exception as e:
            print(f"Error fetching and extracting article content: {e}")
            return {"titles": [], "urls": [], "dates": [], "paragraphs": []}
