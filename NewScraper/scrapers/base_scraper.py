from abc import ABC, abstractmethod
from bs4 import BeautifulSoup
from utils import timing, get_proxy_response
import concurrent.futures

class BaseScraper(ABC):
    def __init__(self, api_key):
        self.api_key = api_key

    def parse_html(self, content):
        return BeautifulSoup(content, "html.parser")

    @abstractmethod
    def extract_news_content(self, soup, main_url):
        pass

    @abstractmethod
    def extract_article_details(self, url):
        pass

    def fetch_and_extract_article(self, url):
        article_response = get_proxy_response(url, self.api_key)
        article_soup = self.parse_html(article_response.content)
        article_details = self.extract_article_details(url)
        article_details["url"] = url
        return article_details

    def get_news_content(self, url):
        response = get_proxy_response(url, self.api_key)
        soup = self.parse_html(response.content)
        news_content = self.extract_news_content(soup, url)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {executor.submit(self.extract_article_details, article_url): article_url for article_url in news_content["urls"]}
            
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    article_text = future.result()
                    index = news_content["urls"].index(url)
                    news_content["paragraphs"][index] = article_text
                except Exception as exc:
                    print(f"{url} generated an exception: {exc}")
        
        return news_content