import type {
  CompanyOverview,
  StockDataPoint,
  NewsItem,
  AlphaVantageResponse,
  TimeSeriesResponse,
  NewsResponse,
  SearchResponse,
} from "@/types/alphavantage";

import {
  createRateLimitError,
  handleApiError,
  isRateLimitResponse,
} from "./error";

const API_KEY = import.meta.env.VITE_ALPHAVANTAGE_API_KEY;
const BASE_URL = "https://www.alphavantage.co/query";

const fetchFromAlphaVantage = async <T>(
  params: Record<string, string>
): Promise<AlphaVantageResponse<T>> => {
  console.log(`🔄 AlphaVantage API Call:`, {
    function: params.function,
    params: { ...params, apikey: "***" },
  });

  try {
    const queryParams = new URLSearchParams({
      ...params,
      apikey: API_KEY,
    });

    const response = await fetch(`${BASE_URL}?${queryParams}`);
    if (!response.ok) {
      throw new Error("Failed to fetch data");
    }
    const data = await response.json();

    if (isRateLimitResponse(data)) {
      throw createRateLimitError();
    }

    if (data["Error Message"]) {
      throw new Error(data["Error Message"]);
    }

    return { data };
  } catch (error) {
    console.error("❌ AlphaVantage Error:", error);
    const apiError = handleApiError(error);
    return {
      data: null,
      error: apiError.message,
      type: apiError.type,
    };
  }
};

interface CompanyData {
  overview: CompanyOverview;
  stockData: StockDataPoint[];
  news: NewsItem[];
}

// Enhanced number formatting utilities
export const formatLargeNumber = (
  value: number | string | undefined | null
): string => {
  // Handle undefined, null, or empty string
  if (value === undefined || value === null || value === "") {
    return "-";
  }

  // Convert string to number if necessary
  const num = typeof value === "string" ? parseFloat(value) : value;

  // Check if the conversion resulted in a valid number
  if (isNaN(num)) {
    return "-";
  }

  try {
    if (Math.abs(num) >= 1e12) {
      return (num / 1e12).toFixed(2) + "T";
    } else if (Math.abs(num) >= 1e9) {
      return (num / 1e9).toFixed(2) + "B";
    } else if (Math.abs(num) >= 1e6) {
      return (num / 1e6).toFixed(2) + "M";
    } else if (Math.abs(num) >= 1e3) {
      return num.toLocaleString();
    }
    return num.toLocaleString();
  } catch (error) {
    console.error("Error formatting number:", error);
    return "-";
  }
};

// Format percentage values safely
export const formatPercentage = (
  value: number | string | undefined | null,
  decimals = 2
): string => {
  if (value === undefined || value === null || value === "") {
    return "-";
  }

  const num = typeof value === "string" ? parseFloat(value) : value;

  if (isNaN(num)) {
    return "-";
  }

  try {
    return `${num.toFixed(decimals)}%`;
  } catch (error) {
    return "-";
  }
};

// Format currency values safely
export const formatCurrency = (
  value: number | string | undefined | null,
  currency = "USD",
  decimals = 2
): string => {
  if (value === undefined || value === null || value === "") {
    return "-";
  }

  const num = typeof value === "string" ? parseFloat(value) : value;

  if (isNaN(num)) {
    return "-";
  }

  try {
    return new Intl.NumberFormat("en-US", {
      style: "currency",
      currency,
      minimumFractionDigits: decimals,
      maximumFractionDigits: decimals,
    }).format(num);
  } catch (error) {
    return "-";
  }
};

/**
 * Fetches all necessary company data in the minimum number of API calls
 * Uses company overview data where possible to avoid redundant calls
 */
export const getCompanyData = async (symbol: string): Promise<CompanyData> => {
  const { data: overview, error: overviewError } =
    await fetchFromAlphaVantage<CompanyOverview>({
      function: "OVERVIEW",
      symbol,
    });

  if (overviewError || !overview) {
    throw new Error(overviewError || "Failed to fetch company overview");
  }

  const { data: timeSeriesData, error: timeSeriesError } =
    await fetchFromAlphaVantage<TimeSeriesResponse>({
      function: "TIME_SERIES_DAILY",
      symbol,
      outputsize: "compact",
    });

  if (timeSeriesError || !timeSeriesData) {
    throw new Error(timeSeriesError || "Failed to fetch time series data");
  }

  const { data: newsData, error: newsError } =
    await fetchFromAlphaVantage<NewsResponse>({
      function: "NEWS_SENTIMENT",
      tickers: symbol,
      limit: "10",
    });

  if (newsError || !newsData) {
    throw new Error(newsError || "Failed to fetch news data");
  }

  return {
    overview,
    stockData: transformTimeSeriesData(timeSeriesData),
    news: transformNewsData(newsData),
  };
};

const transformTimeSeriesData = (
  data: TimeSeriesResponse
): StockDataPoint[] => {
  if (!data["Time Series (Daily)"]) return [];

  return Object.entries(data["Time Series (Daily)"]).map(([date, values]) => ({
    date,
    price: parseFloat(values["4. close"]) || 0,
    volume: parseInt(values["5. volume"], 10) || 0,
    open: parseFloat(values["1. open"]) || 0,
    high: parseFloat(values["2. high"]) || 0,
    low: parseFloat(values["3. low"]) || 0,
    close: parseFloat(values["4. close"]) || 0,
  }));
};

const transformNewsData = (data: NewsResponse): NewsItem[] => {
  if (!data?.feed) return [];

  return data.feed.map((item) => ({
    id: item.url,
    title: item.title,
    summary: item.summary,
    source: item.source,
    url: item.url,
    publishedAt: item.time_published,
    sentiment: item.overall_sentiment_label,
    relatedTickers: item.ticker_sentiment?.map((t) => t.ticker) || [],
  }));
};

export const searchCompany = async (
  query: string
): Promise<AlphaVantageResponse<SearchResponse>> => {
  console.log(`🔄 AlphaVantage Search:`, {
    function: "SYMBOL_SEARCH",
    query,
  });

  try {
    const queryParams = new URLSearchParams({
      function: "SYMBOL_SEARCH",
      keywords: query,
      apikey: API_KEY,
    });

    const response = await fetch(`${BASE_URL}?${queryParams}`);
    const data = await response.json();

    if (data["Error Message"]) {
      throw new Error(data["Error Message"]);
    }
    if (data["Note"]?.includes("API call frequency")) {
      throw new Error("API rate limit exceeded");
    }

    return { data };
  } catch (error) {
    console.error("❌ AlphaVantage Search Error:", error);
    return {
      data: null,
      error: error instanceof Error ? error.message : "Unknown error",
    };
  }
};

export const transformSearchResults = (data: SearchResponse) => {
  if (!data?.bestMatches) return [];

  return data.bestMatches.map((match) => ({
    symbol: match["1. symbol"],
    name: match["2. name"],
    type: match["3. type"],
    region: match["4. region"],
    currency: match["8. currency"],
    matchScore: parseFloat(match["9. matchScore"]) || 0,
  }));
};
