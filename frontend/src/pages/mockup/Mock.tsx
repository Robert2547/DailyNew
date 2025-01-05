// CompanyPage.tsx - Part 1
import { useState } from "react";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Alert, AlertDescription } from "@/components/ui/alert";
import {
  Bell,
  BellOff,
  TrendingUp,
  PieChart,
  Users,
  AlertCircle,
  ExternalLink,
} from "lucide-react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  BarChart,
  Bar,
  AreaChart,
  Area,
} from "recharts";
import { cn } from "@/utils/cn";
import {
  mockCompanyData,
  mockNews,
  mockHistoricalData,
  mockAnalystRatings,
  mockInsiderTransactions,
} from "./mockData";
import { TimeframeType } from "./types";

export const Mock = () => {
  const [isSubscribed, setIsSubscribed] = useState(false);
  const [timeframe, setTimeframe] = useState<TimeframeType>("3M");

  const formatLargeNumber = (num: string | number) => {
    const n = typeof num === "string" ? parseFloat(num) : num;
    if (n >= 1e12) return (n / 1e12).toFixed(2) + "T";
    if (n >= 1e9) return (n / 1e9).toFixed(2) + "B";
    if (n >= 1e6) return (n / 1e6).toFixed(2) + "M";
    return n.toLocaleString();
  };

  const getStockData = () => {
    switch (timeframe) {
      case "1M":
        return mockHistoricalData.monthly.slice(-30);
      case "3M":
        return mockHistoricalData.monthly;
      case "1Y":
        return mockHistoricalData.yearly;
      default:
        return mockHistoricalData.monthly;
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold mb-2">
            {mockCompanyData.Name} ({mockCompanyData.Symbol})
          </h1>
          <p className="text-gray-600">
            {mockCompanyData.Exchange} · {mockCompanyData.Currency}
          </p>
        </div>
        <div className="flex gap-4">
          <Alert className="max-w-xs">
            <AlertCircle className="h-4 w-4" />
            <AlertDescription>
              Market {new Date().getHours() < 16 ? "Open" : "Closed"}
            </AlertDescription>
          </Alert>
          <Button
            onClick={() => setIsSubscribed(!isSubscribed)}
            variant={isSubscribed ? "outline" : "default"}
          >
            {isSubscribed ? (
              <BellOff className="mr-2 h-4 w-4" />
            ) : (
              <Bell className="mr-2 h-4 w-4" />
            )}
            {isSubscribed ? "Unsubscribe" : "Subscribe"}
          </Button>
        </div>
      </div>

      {/* Main Content */}
      <Tabs defaultValue="overview" className="space-y-6">
        <TabsList className="grid w-full grid-cols-4">
          <TabsTrigger value="overview">
            <PieChart className="h-4 w-4 mr-2" />
            Overview
          </TabsTrigger>
          <TabsTrigger value="charts">
            <TrendingUp className="h-4 w-4 mr-2" />
            Charts
          </TabsTrigger>
          <TabsTrigger value="news">
            <Users className="h-4 w-4 mr-2" />
            News & Analysis
          </TabsTrigger>
          <TabsTrigger value="insider">
            <Users className="h-4 w-4 mr-2" />
            Insider Activity 
          </TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview" className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {/* Company Description */}
            <div className="md:col-span-2">
              <Card>
                <CardHeader>
                  <CardTitle>Company Overview</CardTitle>
                  <CardDescription>
                    {mockCompanyData.Sector} · {mockCompanyData.Industry}
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <p className="text-gray-700">{mockCompanyData.Description}</p>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 pt-4 border-t">
                    <div>
                      <p className="text-sm text-gray-500">Founded</p>
                      <p className="font-medium">{mockCompanyData.Founded}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">Headquarters</p>
                      <p className="font-medium">
                        {mockCompanyData.Headquarters}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">Employees</p>
                      <p className="font-medium">
                        {mockCompanyData.EmployeeCount}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">CEO</p>
                      <p className="font-medium">{mockCompanyData.CEO}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>

            {/* Key Stats */}
            <div>
              <Card>
                <CardHeader>
                  <CardTitle>Key Statistics</CardTitle>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    <div>
                      <p className="text-sm text-gray-500">Market Cap</p>
                      <p className="font-medium">
                        $
                        {formatLargeNumber(
                          mockCompanyData.MarketCapitalization
                        )}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">P/E Ratio</p>
                      <p className="font-medium">{mockCompanyData.PERatio}</p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">Revenue (TTM)</p>
                      <p className="font-medium">
                        ${formatLargeNumber(mockCompanyData.RevenueTTM)}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">Profit Margin</p>
                      <p className="font-medium">
                        {mockCompanyData.ProfitMargin}%
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </div>
          </div>

          {/* Stock Chart */}
          <Card>
            <CardHeader>
              <CardTitle>Stock Performance</CardTitle>
              <CardDescription>Last 30 days of trading</CardDescription>
            </CardHeader>
            <CardContent className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={mockHistoricalData.monthly.slice(-30)}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis domain={["auto", "auto"]} />
                  <Tooltip />
                  <Line
                    type="monotone"
                    dataKey="price"
                    stroke="#4f46e5"
                    strokeWidth={2}
                  />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>

          {/* Latest News Preview */}
          <Card>
            <CardHeader>
              <CardTitle>Recent News</CardTitle>
              <CardDescription>
                Latest updates and market coverage
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                {mockNews.slice(0, 3).map((item) => (
                  <div key={item.id} className="border-b last:border-0 pb-4">
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="font-semibold">
                        <a
                          href={item.url}
                          className="hover:text-blue-600 hover:underline"
                        >
                          {item.title}
                        </a>
                      </h3>
                      <span
                        className={cn(
                          "px-2 py-1 rounded-full text-xs font-medium",
                          {
                            "bg-green-100 text-green-800":
                              item.sentiment === "positive",
                            "bg-red-100 text-red-800":
                              item.sentiment === "negative",
                            "bg-gray-100 text-gray-800":
                              item.sentiment === "neutral",
                          }
                        )}
                      >
                        {item.sentiment}
                      </span>
                    </div>
                    <p className="text-sm text-gray-600">{item.summary}</p>
                    <div className="flex justify-between items-center mt-2 text-sm text-gray-500">
                      <span>{item.source}</span>
                      <span>
                        {new Date(item.publishedAt).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
        {/* Charts Tab */}
        <TabsContent value="charts" className="space-y-6">
          <Card>
            <CardHeader>
              <div className="flex justify-between items-center">
                <div>
                  <CardTitle>Price & Volume Analysis</CardTitle>
                  <CardDescription>Historical trading data</CardDescription>
                </div>
                <div className="flex gap-2">
                  <Button
                    variant={timeframe === "1M" ? "default" : "outline"}
                    onClick={() => setTimeframe("1M")}
                  >
                    1M
                  </Button>
                  <Button
                    variant={timeframe === "3M" ? "default" : "outline"}
                    onClick={() => setTimeframe("3M")}
                  >
                    3M
                  </Button>
                  <Button
                    variant={timeframe === "1Y" ? "default" : "outline"}
                    onClick={() => setTimeframe("1Y")}
                  >
                    1Y
                  </Button>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <div className="h-[400px]">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={getStockData()}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis domain={["auto", "auto"]} />
                    <Tooltip />
                    <Line
                      type="monotone"
                      dataKey="price"
                      stroke="#4f46e5"
                      strokeWidth={2}
                      dot={false}
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
              <div className="h-[200px] mt-6">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={getStockData()}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip />
                    <Area
                      type="monotone"
                      dataKey="volume"
                      fill="#e2e8f0"
                      stroke="#94a3b8"
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>

          {/* Analyst Ratings */}
          <Card>
            <CardHeader>
              <CardTitle>Analyst Coverage</CardTitle>
              <CardDescription>
                Latest analyst ratings and price targets
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                {mockAnalystRatings.map((rating, index) => (
                  <div
                    key={index}
                    className="flex justify-between items-center border-b last:border-0 pb-4"
                  >
                    <div>
                      <h4 className="font-medium">{rating.firm}</h4>
                      <p className="text-sm text-gray-600">{rating.date}</p>
                    </div>
                    <div className="text-right">
                      <p className="font-medium">{rating.rating}</p>
                      <p className="text-sm text-gray-600">
                        PT: ${rating.priceTarget}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>
        {/* News Tab */}
        <TabsContent value="news" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Latest News & Analysis</CardTitle>
              <CardDescription>
                Comprehensive news coverage and market analysis
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-8">
                {mockNews.map((item) => (
                  <div key={item.id} className="border-b last:border-0 pb-8">
                    <div className="flex justify-between items-start mb-3">
                      <h3 className="text-lg font-semibold">
                        <a
                          href={item.url}
                          className="hover:text-blue-600 hover:underline inline-flex items-center"
                        >
                          {item.title}
                          <ExternalLink className="ml-2 h-4 w-4" />
                        </a>
                      </h3>
                      <span
                        className={cn(
                          "px-2 py-1 rounded-full text-xs font-medium",
                          {
                            "bg-green-100 text-green-800":
                              item.sentiment === "positive",
                            "bg-red-100 text-red-800":
                              item.sentiment === "negative",
                            "bg-gray-100 text-gray-800":
                              item.sentiment === "neutral",
                          }
                        )}
                      >
                        {item.sentiment}
                      </span>
                    </div>
                    <p className="text-gray-700 mb-3">{item.summary}</p>
                    <div className="flex justify-between items-center text-sm text-gray-500">
                      <span className="font-medium">{item.source}</span>
                      <span>
                        {new Date(item.publishedAt).toLocaleDateString()}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Insider Activity Tab */}
        <TabsContent value="insider" className="space-y-6">
          <Card>
            <CardHeader>
              <CardTitle>Insider Transactions</CardTitle>
              <CardDescription>Recent insider trading activity</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                {mockInsiderTransactions.map((transaction, index) => (
                  <div key={index} className="border-b last:border-0 pb-4">
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <h4 className="font-semibold">
                          {transaction.insiderName}
                        </h4>
                        <p className="text-sm text-gray-600">
                          {transaction.title}
                        </p>
                      </div>
                      <div className="text-right">
                        <span
                          className={`inline-block px-2 py-1 rounded text-sm ${
                            transaction.transactionType === "Buy"
                              ? "bg-green-100 text-green-800"
                              : "bg-red-100 text-red-800"
                          }`}
                        >
                          {transaction.transactionType}
                        </span>
                      </div>
                    </div>
                    <div className="grid grid-cols-3 gap-4 text-sm">
                      <div>
                        <p className="text-gray-500">Date</p>
                        <p className="font-medium">{transaction.date}</p>
                      </div>
                      <div>
                        <p className="text-gray-500">Shares</p>
                        <p className="font-medium">
                          {formatLargeNumber(transaction.shares)}
                        </p>
                      </div>
                      <div>
                        <p className="text-gray-500">Value</p>
                        <p className="font-medium">
                          ${formatLargeNumber(transaction.totalValue)}
                        </p>
                      </div>
                      <div>
                        <p className="text-gray-500">Price/Share</p>
                        <p className="font-medium">
                          ${transaction.pricePerShare.toFixed(2)}
                        </p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Insider Trading Summary</CardTitle>
              <CardDescription>Last 12 months activity</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-semibold mb-4">Buy/Sell Ratio</h4>
                  <div className="h-[200px]">
                    <ResponsiveContainer width="100%" height="100%">
                      <BarChart
                        data={[
                          {
                            type: "Buys",
                            value: mockInsiderTransactions.filter(
                              (t) => t.transactionType === "Buy"
                            ).length,
                          },
                          {
                            type: "Sells",
                            value: mockInsiderTransactions.filter(
                              (t) => t.transactionType === "Sell"
                            ).length,
                          },
                        ]}
                      >
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="type" />
                        <YAxis />
                        <Tooltip />
                        <Bar dataKey="value" fill="#4f46e5" />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                </div>
                <div>
                  <h4 className="font-semibold mb-4">Transaction Volume</h4>
                  <div className="space-y-4">
                    <div>
                      <p className="text-sm text-gray-500">Total Buy Volume</p>
                      <p className="font-medium">
                        $
                        {formatLargeNumber(
                          mockInsiderTransactions
                            .filter((t) => t.transactionType === "Buy")
                            .reduce((acc, curr) => acc + curr.totalValue, 0)
                        )}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">Total Sell Volume</p>
                      <p className="font-medium">
                        $
                        {formatLargeNumber(
                          mockInsiderTransactions
                            .filter((t) => t.transactionType === "Sell")
                            .reduce((acc, curr) => acc + curr.totalValue, 0)
                        )}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-gray-500">
                        Average Transaction Size
                      </p>
                      <p className="font-medium">
                        $
                        {formatLargeNumber(
                          mockInsiderTransactions.reduce(
                            (acc, curr) => acc + curr.totalValue,
                            0
                          ) / mockInsiderTransactions.length
                        )}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};
