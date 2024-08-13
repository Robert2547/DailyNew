from urllib.parse import urljoin
from scrapers.base_scraper import BaseScraper
from config import SOURCES
from utils import is_within_last_24_hours
import requests
import concurrent.futures
from newspaper import Article
from utils import timing


class YahooScraper(BaseScraper):
    def __init__(self, api_key):
        super().__init__(api_key)
        self.config = SOURCES["yahooFinance"]

    def extract_news_content(self, soup, main_url):
        content = {"titles": [], "urls": [], "dates": [], "paragraphs": []}
        sections = soup.select(self.config["company"]["sections"])
        
        for section in sections:
            title_element = section.select_one(self.config["company"]["titles"])
            url_element = section.select_one(self.config["company"]["urls"])
            date_element = section.select_one(self.config["company"]["dates"])
            
            if title_element and url_element and date_element:
                title = title_element.get_text(strip=True)
                url = url_element.get('href')
                date = date_element.get_text(strip=True)
                
                time_parts = date.split('•')
                if len(time_parts) > 1:
                    time_ago = time_parts[-1].strip()
                    if is_within_last_24_hours(time_ago):
                        content["titles"].append(title)
                        content["urls"].append(urljoin(main_url, url))
                        content["dates"].append(date)
                        content["paragraphs"].append("")
        return content

    def extract_article_details(self, url):
        article = Article(url)
        article.download()
        article.parse()
        return article.text         

    def get_news_content(self, url):
        response = requests.get(url)
        soup = self.parse_html(response.content)
        try:
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
        except Exception as e:
            print(f"Error extracting news content: {e}")
            news_content = {"titles": [], "urls": [], "dates": [], "paragraphs": []}
            return news_content