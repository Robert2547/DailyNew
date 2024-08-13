from urllib.parse import urljoin
from config.source_configs import SOURCES
from scrapers.base_scraper import BaseScraper

class ReutersScraper(BaseScraper):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.config = SOURCES["reuters"]

    # Grab all the recent articles for a given ticker, TODO: First we need to check if the following is within 24 hours
    def extract_news_content(self, soup, main_url):
        selectors = self.config["company"]
        content = {}

        for key, selector in selectors.items():
            elements = soup.select(selector)
            if key == "urls":
                content[key] = [urljoin(main_url, url["href"]) for url in elements] if elements else None
            elif key == "category":
                content[key] = [topic.get_text(strip=True).rstrip("category") for topic in elements] if elements else None
            else:
                content[key] = [element.get_text(strip=True) for element in elements] if elements else None
        return content

    def extract_article_details(self, soup):
        selectors = self.config["article"]
        content = {}

        for key, selector in selectors.items():
            if key == "paragraphs":
                elements = soup.select(selector)
                content[key] = [p.get_text(strip=True) for p in elements]
            else:
                element = soup.select_one(selector)
                content[key] = element.get_text(strip=True) if element else None

        return content