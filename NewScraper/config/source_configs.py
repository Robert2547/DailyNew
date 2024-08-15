HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Cache-Control": "max-age=0",
}


SOURCES = {
    "reuters": {
        "base_url": "https://www.reuters.com/markets/companies",
        "headers": HEADERS,
        "company": {
            "titles": ".media-story-card__headline__tFMEu[href]",
            "urls": ".media-story-card__headline__tFMEu[href]",
            "dates": ".media-story-card__body__3tRWy time",
            "category": ".media-story-card__section__SyzYF a",
        },
        "article": {
            "title": 'h1[data-testid="Heading"]',
            "paragraphs": 'div[data-testid*="paragraph-"]',
        },
    },
    "yahooFinance": {
        "base_url": "https://finance.yahoo.com/quote/{ticker}",
        "headers": HEADERS,
        "company": {
            "sections": "section.container.sz-small.block.yf-1044anq.responsive.hideImageSmScreen",
            "titles": "h3.clamp.yf-1044anq",
            "urls": "a.subtle-link.fin-size-small.titles.noUnderline.yf-13p9sh2",
            "dates": "div.publishing.font-condensed.yf-da5pxu",
        },
        "article": {
            "title": "h1[data-testid='Heading']",
            "date": "time > span:nth-child(2)",
            "paragraphs": "div[data-testid*='paragraph-']",
        },
    },
    "marketWatch": {
        "base_url": "https://www.marketwatch.com/investing/stock/{ticker}?mod=mw_quote_tab",
        "headers": HEADERS,
        "company": {
            "titles": "h3.article__headline",
            "urls": "h3.article__headline a.link",
            "dates": "span.article__timestamp",
        },
    },
    # Add more sources as needed
}
