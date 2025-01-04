// mockData.ts
import {
  CompanyOverview,
  NewsItem,
  InsiderTransaction,
  AnalystRating,
  StockDataPoint,
} from "./types";

export const mockCompanyData: CompanyOverview = {
  Symbol: "AAPL",
  Name: "Apple Inc.",
  Description:
    "Apple Inc. designs, manufactures, and markets smartphones, personal computers, tablets, wearables, and accessories worldwide. The company offers iPhone, iPad, Mac, Apple Watch, and related services. Known for innovation and brand loyalty, Apple has transformed multiple industries including mobile communications, personal computing, and digital entertainment.",
  Exchange: "NASDAQ",
  Currency: "USD",
  Country: "United States",
  Sector: "Technology",
  Industry: "Consumer Electronics",
  MarketCapitalization: "3000000000000",
  PERatio: "28.5",
  DividendYield: "0.52",
  "52WeekHigh": "198.23",
  "52WeekLow": "124.17",
  Beta: "1.2",
  SharesOutstanding: "15700000000",
  EPS: "6.42",
  RevenueTTM: "383700000000",
  ProfitMargin: "25.31",
  CEO: "Tim Cook",
  EmployeeCount: "164,000",
  Founded: "1976",
  Headquarters: "Cupertino, California",
};

export const mockNews: NewsItem[] = [
  {
    id: "1",
    title: "Apple Vision Pro Set to Launch February 2nd, Starting at $3,499",
    summary:
      "Apple has announced that its highly anticipated Vision Pro mixed-reality headset will be available for purchase starting February 2nd. Pre-orders begin January 19th, marking Apple's first major new product category since the Apple Watch.",
    source: "Bloomberg",
    url: "#",
    publishedAt: "2024-01-08T14:30:00Z",
    sentiment: "positive",
    relatedTickers: ["AAPL"],
  },
  {
    id: "2",
    title: "Apple Becomes First Company to Hit $3 Trillion Market Value",
    summary:
      "Apple Inc. achieved another milestone by becoming the first company to reach a $3 trillion market capitalization, highlighting the tech giant's dominance and continued growth in the global market.",
    source: "Financial Times",
    url: "#",
    publishedAt: "2024-01-07T09:15:00Z",
    sentiment: "positive",
    relatedTickers: ["AAPL"],
  },
  {
    id: "3",
    title: "New iPhone 16 Production Details Leak, Suggesting AI Focus",
    summary:
      "Supply chain sources reveal Apple's upcoming iPhone 16 series will feature enhanced AI capabilities and a new chip design optimized for on-device artificial intelligence processing.",
    source: "Reuters",
    url: "#",
    publishedAt: "2024-01-06T16:45:00Z",
    sentiment: "neutral",
    relatedTickers: ["AAPL"],
  },
  {
    id: "4",
    title: "Apple's Services Revenue Hits New Record in Q4",
    summary:
      "Apple's services segment, including App Store, Apple Music, and iCloud, continues to show strong growth, reaching new revenue records and highlighting the company's successful diversification strategy.",
    source: "Wall Street Journal",
    url: "#",
    publishedAt: "2024-01-05T11:20:00Z",
    sentiment: "positive",
    relatedTickers: ["AAPL"],
  },
];

// Generate mock stock data
export const generateMockPriceData = (
  days: number,
  basePrice: number,
  volatility: number
): StockDataPoint[] => {
  return Array.from({ length: days }, (_, i) => {
    const date = new Date();
    date.setDate(date.getDate() - (days - i));
    const randomChange = (Math.random() - 0.5) * volatility;
    const price = basePrice + randomChange;

    return {
      date: date.toISOString().split("T")[0],
      price: Number(price.toFixed(2)),
      volume: Math.round(20000000 + Math.random() * 30000000),
      open: Number((price - randomChange / 2).toFixed(2)),
      high: Number((price + Math.abs(randomChange)).toFixed(2)),
      low: Number((price - Math.abs(randomChange)).toFixed(2)),
      close: Number(price.toFixed(2)),
    };
  });
};

export const mockHistoricalData = {
  daily: generateMockPriceData(30, 185, 3),
  weekly: generateMockPriceData(52, 185, 5),
  monthly: generateMockPriceData(90, 185, 8),
  yearly: generateMockPriceData(365, 185, 12),
};

export const mockAnalystRatings: AnalystRating[] = [
  {
    firm: "Morgan Stanley",
    rating: "Overweight",
    priceTarget: 220,
    date: "2024-01-05",
  },
  {
    firm: "Goldman Sachs",
    rating: "Buy",
    priceTarget: 225,
    date: "2024-01-03",
  },
  {
    firm: "JP Morgan",
    rating: "Overweight",
    priceTarget: 215,
    date: "2024-01-02",
  },
  {
    firm: "Bank of America",
    rating: "Buy",
    priceTarget: 210,
    date: "2023-12-28",
  },
];


export const mockInsiderTransactions: InsiderTransaction[] = [
  {
    date: "2024-01-05",
    insiderName: "Tim Cook",
    title: "Chief Executive Officer",
    transactionType: "Sell",
    shares: 150000,
    pricePerShare: 185.25,
    totalValue: 27787500,
  },
  {
    date: "2024-01-03",
    insiderName: "Luca Maestri",
    title: "Chief Financial Officer",
    transactionType: "Sell",
    shares: 75000,
    pricePerShare: 186.02,
    totalValue: 13951500,
  },
  {
    date: "2023-12-28",
    insiderName: "Jeff Williams",
    title: "Chief Operating Officer",
    transactionType: "Buy",
    shares: 25000,
    pricePerShare: 184.75,
    totalValue: 4618750,
  },
  {
    date: "2023-12-15",
    insiderName: "Katherine Adams",
    title: "General Counsel",
    transactionType: "Buy",
    shares: 15000,
    pricePerShare: 183.5,
    totalValue: 2752500,
  },
  {
    date: "2023-12-10",
    insiderName: "Deirdre O'Brien",
    title: "Senior VP, Retail + People",
    transactionType: "Sell",
    shares: 45000,
    pricePerShare: 182.75,
    totalValue: 8223750,
  },
  {
    date: "2023-12-05",
    insiderName: "Craig Federighi",
    title: "Senior VP, Software Engineering",
    transactionType: "Sell",
    shares: 35000,
    pricePerShare: 181.5,
    totalValue: 6352500,
  },
];
