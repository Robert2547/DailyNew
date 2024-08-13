"""
Module for handling article content extraction and processing.
"""

from bs4 import BeautifulSoup
import aiohttp
from fastapi import HTTPException
import validators

async def fetch_article_content(url: str) -> str:
    """
    Asynchronously fetch the content of an article from a given URL.
    """
    if not validators.url(url):
        raise HTTPException(status_code=400, detail="Invalid URL")
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                raise HTTPException(status_code=response.status, detail="Failed to fetch article content")
            return await response.text()



def extract_article_content(html_content: str) -> str:
    """
    Extract the main content from HTML using BeautifulSoup.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    article = soup.find("article") or soup.find("div", class_="article-content")

    if article:
        content = []
        for element in article.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6"]):
            content.append(element.get_text().strip())
        return " ".join(content)
    else:
        body = soup.find("body")
        if body:
            content = []
            for element in body.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6"]):
                content.append(element.get_text().strip())
            return " ".join(content)
        else:
            return " ".join(soup.stripped_strings)


async def get_content(url: str) -> str:
    """
    Get content from a URL.
    """
    html_content = await fetch_article_content(url)
    content = extract_article_content(html_content)
    if not content.strip():
        raise HTTPException(status_code=400, detail="Failed to extract content from URL")
    return content
