// src/types/alphavantage.ts

export interface CompanyOverview {
  Symbol: string;
  Name: string;
  Description: string;
  Exchange: string;
  Currency: string;
  Country: string;
  Sector: string;
  Industry: string;
  MarketCapitalization: string;
  PERatio: string;
  DividendYield: string;
  "52WeekHigh": string;
  "52WeekLow": string;
  Beta: string;
  SharesOutstanding: string;
  EPS: string;
  RevenueTTM: string;
  ProfitMargin: string;
}

export interface StockDataPoint {
  date: string;
  price: number;
  volume: number;
  open: number;
  high: number;
  low: number;
  close: number;
}

export interface NewsItem {
  id: string;
  title: string;
  summary: string;
  source: string;
  url: string;
  publishedAt: string;
  sentiment: "positive" | "negative" | "neutral";
  relatedTickers?: string[];
}

// API Response Types
export interface AlphaVantageResponse<T> {
  data: T | null;
  error?: string;
}

export interface TimeSeriesResponse {
  "Meta Data": {
    "1. Information": string;
    "2. Symbol": string;
    "3. Last Refreshed": string;
    "4. Output Size": string;
    "5. Time Zone": string;
  };
  "Time Series (Daily)": {
    [date: string]: {
      "1. open": string;
      "2. high": string;
      "3. low": string;
      "4. close": string;
      "5. volume": string;
    };
  };
}

export interface NewsResponse {
  items: string;
  sentiment_score_definition: string;
  relevance_score_definition: string;
  feed: Array<{
    title: string;
    url: string;
    time_published: string;
    summary: string;
    source: string;
    overall_sentiment_score: number;
    overall_sentiment_label: "positive" | "negative" | "neutral";
    ticker_sentiment: Array<{
      ticker: string;
      relevance_score: string;
      ticker_sentiment_score: string;
      ticker_sentiment_label: string;
    }>;
  }>;
}

export interface SearchMatch {
  "1. symbol": string;
  "2. name": string;
  "3. type": string;
  "4. region": string;
  "5. marketOpen": string;
  "6. marketClose": string;
  "7. timezone": string;
  "8. currency": string;
  "9. matchScore": string;
}

export interface SearchResponse {
  bestMatches: SearchMatch[];
}
