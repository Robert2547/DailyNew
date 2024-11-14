from urllib.parse import urljoin
from app.scrapers import BaseScraper
from app.utils import timing, get_proxy_response

class ReutersScraper(BaseScraper):
    def __init__(self, config, use_headers=False):
        super().__init__(config, use_headers)
        
    def get_url(self, ticker):
        return self.config["base_url"].format(ticker=ticker)

    @timing
    def extract_news_content(self, soup, main_url):
        selectors = self.config["company"]
        content = {"titles": [], "urls": [], "dates": [], "paragraphs": []}
        print("ReutersScraper extract_news_content")
        print("Length of selectors: ", len(selectors))
        for key, selector in selectors.items():
            elements = soup.select(selector)
            if key == "urls":
                content[key] = [urljoin(main_url, url["href"]) for url in elements] if elements else []
            elif key == "dates":
                content[key] = [self.standardize_date(date.get_text(strip=True)) for date in elements] if elements else []
            else:  # titles
                content[key] = [element.get_text(strip=True) for element in elements] if elements else []
        
        content["paragraphs"] = [""] * len(content["urls"])  # Initialize with empty strings
        return content

    def extract_article_details(self, soup):
        selectors = self.config["article"]
        content = {}

        for key, selector in selectors.items():
            if key == "paragraphs":
                elements = soup.select(selector)
                content[key] = "\n".join([p.get_text(strip=True) for p in elements])
            else:
                element = soup.select_one(selector)
                content[key] = element.get_text(strip=True) if element else None

        return content


   