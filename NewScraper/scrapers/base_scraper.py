from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from utils import timing, get_proxy_response
import concurrent.futures
from config import HEADERS
from newspaper import Article
from urllib.parse import urljoin
from datetime import datetime
import requests

class BaseScraper(ABC):
    def __init__(self, config, use_headers=True):
        self.config = config
        self.base_url = config.get("base_url", "")
        self.headers = config.get("headers", {}) if use_headers else {}

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
        soup = self.parse_html(response.content)
        
        try:
            news_content = self.extract_news_content(soup, url)
            self.fetch_article_contents(news_content)
            return news_content
        except Exception as e:
            print(f"Error extracting news content: {e}")
            return {"titles": [], "urls": [], "dates": [], "paragraphs": []}


    def fetch_article_contents(self, news_content):
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {executor.submit(self.extract_article_details, article_url): article_url 
                             for article_url in news_content["urls"]}
            
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    article_text = future.result()
                    index = news_content["urls"].index(url)
                    news_content["paragraphs"][index] = article_text
                except Exception as exc:
                    print(f"{url} generated an exception: {exc}")




