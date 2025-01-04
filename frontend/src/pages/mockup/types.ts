// types.ts
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
    CEO: string;
    EmployeeCount: string;
    Founded: string;
    Headquarters: string;
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
    sentiment: 'positive' | 'negative' | 'neutral';
    relatedTickers?: string[];
    imageUrl?: string;
  }
  
  export interface InsiderTransaction {
    date: string;
    insiderName: string;
    title: string;
    transactionType: 'Buy' | 'Sell';
    shares: number;
    pricePerShare: number;
    totalValue: number;
  }
  
  export interface AnalystRating {
    firm: string;
    rating: string;
    priceTarget: number;
    date: string;
  }
  
  export type TimeframeType = '1D' | '1W' | '1M' | '3M' | 'YTD' | '1Y' | 'ALL';