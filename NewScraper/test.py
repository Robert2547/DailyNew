import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from newspaper import Article
import concurrent.futures
from pathlib import Path
import json
from functools import wraps
import time

def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"{func.__name__} took {end_time - start_time:.2f} seconds to execute.")
        return result
    return wrapper

def is_within_24_hours(time_str):
    try:
        now = datetime.now()
        if 'ago' not in time_str.lower():
            return False
        
        time_parts = time_str.split()
        number = int(time_parts[0])
        unit = time_parts[1]

        if unit.startswith("hour"):
            delta = timedelta(hours=number)
        elif unit.startswith("minute"):
            delta = timedelta(minutes=number)
        elif unit.startswith("second"):
            delta = timedelta(seconds=number)
        elif unit.startswith("day"):
            delta = timedelta(days=number)
        else:
            return False

        return delta <= timedelta(hours=24)
    except Exception as e:
        print(f"Error in is_within_24_hours: {e}")
        return False

def scrape_yahoo_article(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        print(f"Error scraping article: {e}")
        return None

def get_yahoo_soup(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.content, "html.parser")
    except requests.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

def scrape_yahoo(url):
    soup = get_yahoo_soup(url)
    if not soup:
        return []

    article_data = []
    
    sections = soup.find_all("section", class_="container sz-small block yf-1044anq responsive hideImageSmScreen")
    
    for section in sections:
        title_element = section.find("h3", class_="clamp yf-1044anq")
        link_element = section.find("a", class_="subtle-link fin-size-small titles noUnderline yf-13p9sh2")
        time_element = section.find("div", class_="publishing font-condensed yf-da5pxu")
        
        if title_element and link_element and time_element:
            title = title_element.text.strip()
            article_url = link_element['href']
            if not article_url.startswith('http'):
                article_url = f"https://finance.yahoo.com{article_url}"
            
            time_text = time_element.text.strip()
            time_parts = time_text.split('•')
            if len(time_parts) > 1:
                time_ago = time_parts[-1].strip()
                if is_within_24_hours(time_ago):
                    print("Time ago:", time_ago)
                    article_data.append((article_url, title, time_text))
    
    return article_data

def process_article(article_info):
    url, title, time_text = article_info
    article_text = scrape_yahoo_article(url)
    return {
        "url": url,
        "title": title,
        "time": time_text,
        "text": article_text[:1000] if article_text else None  # Limit to first 1000 characters
    }

@timing_decorator
def main():
    URL = "https://finance.yahoo.com/quote/AVGO/"
    recent_articles = scrape_yahoo(URL)

    if not recent_articles:
        print("No recent articles found within the last 24 hours.")
        return

    output_folder = Path("output")
    output_folder.mkdir(exist_ok=True)
    output_file = output_folder / "articles.json"

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(process_article, recent_articles))

    # # Save results to JSON file
    # with output_file.open("w", encoding="utf-8") as f:
    #     json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"Processed {len(results)} articles. Results saved to {output_file}")

if __name__ == "__main__":
    main()