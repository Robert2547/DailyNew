SOURCES = {
    "reuters": {
        "base_url": "https://www.reuters.com/markets/companies",
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
        "base_url": "https://finance.yahoo.com/quote/",
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
    # Add more sources as needed
}
