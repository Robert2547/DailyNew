from scrapers.base_scraper import BaseScraper
from datetime import datetime, timedelta

class YahooScraper(BaseScraper):
    """
    A scraper class for extracting financial news from Yahoo Finance.
    
    This scraper is designed to fetch news articles related to specific stock tickers
    from Yahoo Finance. It inherits from BaseScraper and implements specific logic
    for parsing Yahoo Finance's HTML structure.
    
    Attributes:
        config (dict): Configuration dictionary containing selectors and URLs
        headers (dict): HTTP headers for requests
    """

    def __init__(self, config, use_headers=False):
        """
        Initialize the Yahoo Finance scraper.

        Args:
            config (dict): Configuration dictionary containing base_url and HTML selectors
            use_headers (bool, optional): Whether to use custom headers for requests. Defaults to False
        """
        super().__init__(config, use_headers)
        
    def extract_news_content(self, soup, main_url):
        """
        Extract news articles from the Yahoo Finance page.

        This method parses the HTML content to find and extract news articles including
        their titles, URLs, and publication dates.

        Args:
            soup (BeautifulSoup): Parsed HTML content
            main_url (str): The URL being scraped

        Returns:
            dict: Dictionary containing lists of titles, URLs, dates, and paragraphs with the structure:
                {
                    "titles": List[str],
                    "urls": List[str],
                    "dates": List[str],
                    "paragraphs": List[str]
                }
        """
        content = {"titles": [], "urls": [], "dates": [], "paragraphs": []}
        
        # Find the main news section using configured selector
        parent_section = soup.select_one(self.config["company"]["section"])
        if parent_section:
            # Get all news item divs
            news_items = parent_section.find_all('div', recursive=False)
            print("Length of news items: ", len(news_items))
            
            for i, item in enumerate(news_items, 1):
                try:
                    # Extract title
                    title_elem = item.select_one(self.config["company"]["titles"])
                    if not title_elem:
                        continue
                    
                    # Extract URL
                    url_elem = item.select_one(self.config["company"]["urls"])
                    if not url_elem:
                        continue
                        
                    title = title_elem.get_text(strip=True)
                    url = url_elem.get('href')
                    # Ensure absolute URL
                    if not url.startswith('http'):
                        url = f"https://finance.yahoo.com{url}"
                    
                    # Extract and parse date
                    date_elem = item.select_one(self.config["company"]["dates"])
                    if not date_elem:
                        continue
                        
                    date_text = date_elem.get_text(strip=True)
                    standardized_date = self.standardize_date(date_text)
                    
                    # Only include recent articles
                    if self.is_recent_article(standardized_date):
                        content["titles"].append(title)
                        content["urls"].append(url)
                        content["dates"].append(standardized_date)
                        content["paragraphs"].append("")
                
                except Exception as e:
                    print(f"Error processing news item {i}: {e}")
                    continue
        else:
            print("News section not found")
        
        return content

    def get_url(self, ticker):
        """
        Generate the URL for a specific stock ticker.

        Args:
            ticker (str): Stock ticker symbol (e.g., 'AAPL')

        Returns:
            str: Complete URL for the ticker's Yahoo Finance page
        """
        return f"{self.config['base_url'].format(ticker=ticker)}"

    def standardize_date(self, date_string):
        """
        Convert Yahoo Finance's relative dates to standardized datetime strings.

        Handles various date formats including:
        - "X minutes ago"
        - "X hours ago"
        - "X days ago"
        - "yesterday"

        Args:
            date_string (str): Raw date string from Yahoo Finance

        Returns:
            str: Standardized date in format "YYYY-MM-DD HH:MM:SS"
        """
        now = datetime.now()
        
        try:
            time_parts = date_string.split('•')
            if len(time_parts) > 1:
                date_part = time_parts[-1].strip()
                
                if 'minute' in date_part or 'hour' in date_part:
                    return now.strftime("%Y-%m-%d %H:%M:%S")
                elif 'day' in date_part:
                    days = int(date_part.split()[0])
                    date = now - timedelta(days=days)
                    return date.strftime("%Y-%m-%d %H:%M:%S")
                elif 'yesterday' in date_part.lower():
                    date = now - timedelta(days=1)
                    return date.strftime("%Y-%m-%d %H:%M:%S")
            
            return now.strftime("%Y-%m-%d %H:%M:%S")
            
        except Exception as e:
            print(f"Error standardizing date {date_string}: {e}")
            return now.strftime("%Y-%m-%d %H:%M:%S")