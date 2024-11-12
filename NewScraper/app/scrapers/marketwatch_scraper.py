from scrapers.base_scraper import BaseScraper
from datetime import datetime, timedelta

class MarketWatchScraper(BaseScraper):
    def __init__(self, config, use_headers=True):
        super().__init__(config, use_headers)
    
    def extract_news_content(self, soup, main_url):
        content = {"titles": [], "urls": [], "dates": [], "paragraphs": []}
        title_elements = soup.select(self.config["company"]["titles"])
        url_elements = soup.select(self.config["company"]["urls"])
        date_elements = soup.select(self.config["company"]["dates"])
        

        for title_element, url_element, date_element in zip(title_elements, url_elements, date_elements):
            if title_element and url_element:
                title = title_element.get_text(strip=True)
                url = url_element.get('href')
                date = date_element.get_text(strip=True)
                standardized_date = self.standardize_date(date)
                if self.is_recent_article(standardized_date):
                    content["titles"].append(title)
                    content["urls"].append(url)
                    content["dates"].append(standardized_date)
                    content["paragraphs"].append("")
                else:
                    break  # Stop processing older articles
        return content

    def get_url(self, ticker):
        return self.config["base_url"].format(ticker=ticker)
    
    def standardize_date(self, date_string):
        now = datetime.now()
        if "min" in date_string or "hour" in date_string:
            return now.strftime("%Y-%m-%d %H:%M:%S")
        elif "day" in date_string:
            days = int(date_string.split()[0])
            date = now - timedelta(days=days)
            return date.strftime("%Y-%m-%d %H:%M:%S")
        else:
            try:
                date = datetime.strptime(date_string, "%b. %d, %Y")
                return date.strftime("%Y-%m-%d %H:%M:%S")
            except ValueError:
                return now.strftime("%Y-%m-%d %H:%M:%S")