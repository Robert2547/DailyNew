// src/services/alphavantage.ts
import type {
  CompanyOverview,
  StockDataPoint,
  NewsItem,
  AlphaVantageResponse,
  TimeSeriesResponse,
  NewsResponse,
} from "@/types/alphavantage";

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
    const data = await response.json();

    if (data["Error Message"]) {
      throw new Error(data["Error Message"]);
    }
    if (data["Note"]?.includes("API call frequency")) {
      throw new Error("API rate limit exceeded");
    }

    return { data };
  } catch (error) {
    console.error("❌ AlphaVantage Error:", error);
    return {
      data: null,
      error: error instanceof Error ? error.message : "Unknown error",
    };
  }
};

interface CompanyData {
  overview: CompanyOverview;
  stockData: StockDataPoint[];
  news: NewsItem[];
}

/**
 * Fetches all necessary company data in the minimum number of API calls
 * Uses company overview data where possible to avoid redundant calls
 */
export const getCompanyData = async (symbol: string): Promise<CompanyData> => {
  // Get company overview first as it contains most fundamental data
  const { data: overview, error: overviewError } =
    await fetchFromAlphaVantage<CompanyOverview>({
      function: "OVERVIEW",
      symbol,
    });

  if (overviewError || !overview) {
    throw new Error(overviewError || "Failed to fetch company overview");
  }

  // Get time series data for stock price information
  const { data: timeSeriesData, error: timeSeriesError } =
    await fetchFromAlphaVantage<TimeSeriesResponse>({
      function: "TIME_SERIES_DAILY",
      symbol,
      outputsize: "compact",
    });

  if (timeSeriesError || !timeSeriesData) {
    throw new Error(timeSeriesError || "Failed to fetch time series data");
  }

  // Get news and sentiment data
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

// Transform time series data into StockDataPoint format
const transformTimeSeriesData = (
  data: TimeSeriesResponse
): StockDataPoint[] => {
  if (!data["Time Series (Daily)"]) return [];

  return Object.entries(data["Time Series (Daily)"]).map(([date, values]) => ({
    date,
    price: parseFloat(values["4. close"]),
    volume: parseInt(values["5. volume"], 10),
    open: parseFloat(values["1. open"]),
    high: parseFloat(values["2. high"]),
    low: parseFloat(values["3. low"]),
    close: parseFloat(values["4. close"]),
  }));
};

// Transform news data into NewsItem format
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

// Helper function to format large numbers consistently
export const formatLargeNumber = (num: string | number) => {
  const n = typeof num === "string" ? parseFloat(num) : num;
  if (n >= 1e12) return (n / 1e12).toFixed(2) + "T";
  if (n >= 1e9) return (n / 1e9).toFixed(2) + "B";
  if (n >= 1e6) return (n / 1e6).toFixed(2) + "M";
  return n.toLocaleString();
};
