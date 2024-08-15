from scrapers.base_scraper import BaseScraper
from datetime import datetime, timedelta


class YahooScraper(BaseScraper):
    def __init__(self, config, use_headers=False):
        super().__init__(config, use_headers)
        
    # Grab list of articles within the last 24 hours
    def extract_news_content(self, soup, main_url):
        content = {"titles": [], "urls": [], "dates": [], "paragraphs": []}
        sections = soup.select(self.config["company"]["sections"])
        for section in sections:
            title_element = section.select_one(self.config["company"]["titles"])
            url_element = section.select_one(self.config["company"]["urls"])
            date_element = section.select_one(self.config["company"]["dates"])

            if title_element and url_element and date_element:
                title = title_element.get_text(strip=True)
                url = url_element.get("href")
                date = date_element.get_text(strip=True)

                time_parts = date.split("•")
                if len(time_parts) > 1:
                    time_ago = time_parts[-1].strip()
                    standardized_date = self.standardize_date(time_ago)
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
        if "minute" in date_string or "hour" in date_string:
            return now.strftime("%Y-%m-%d %H:%M:%S")
        elif "day" in date_string:
            days = int(date_string.split()[0])
            date = now - timedelta(days=days)
            return date.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return now.strftime("%Y-%m-%d %H:%M:%S")
