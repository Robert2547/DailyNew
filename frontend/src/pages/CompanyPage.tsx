import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useQuery } from "@tanstack/react-query";
import * as AlphaVantageService from "@/services/alphaVantage";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { Bell, BellOff, TrendingUp, PieChart, Users } from "lucide-react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { cn } from "@/utils/cn";

export const CompanyPage = () => {
  const { symbol } = useParams<{ symbol: string }>();
  const navigate = useNavigate();
  const [isSubscribed, setIsSubscribed] = useState(false);

  const { data, isLoading, error } = useQuery({
    queryKey: ["company", symbol],
    queryFn: async () => {
      if (!symbol) throw new Error("No symbol provided");
      return AlphaVantageService.getCompanyData(symbol);
    },
    enabled: !!symbol,
    retry: false, // Don't retry on error
  });

  // Handle errors with useEffect
  useEffect(() => {
    if (error) {
      if (error instanceof Error && error.message.includes("rate limit")) {
        navigate("/error", { state: { type: "RATE_LIMIT" } });
      } else {
        navigate("/error", {
          state: {
            type: "API_ERROR",
            message: "Failed to load company data",
          },
        });
      }
    }
  }, [error, navigate]);

  if (isLoading) {
    return (
      <div className="flex justify-center items-center min-h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  if (!data) return null;

  const { overview, stockData, news } = data;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Rest of your component remains the same */}
      {/* Header */}
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold mb-2">
            {overview.Name} ({overview.Symbol})
          </h1>
          <p className="text-gray-600">
            {overview.Exchange} · {overview.Currency}
          </p>
        </div>
        <div className="flex gap-4">
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
        <TabsList className="grid w-full grid-cols-3">
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
            News
          </TabsTrigger>
        </TabsList>

        {/* Overview Tab */}
        <TabsContent value="overview">
          <Card>
            <CardHeader>
              <CardTitle>Company Overview</CardTitle>
              <CardDescription>
                {overview.Sector} · {overview.Industry}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-gray-700 mb-6">{overview.Description}</p>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div>
                  <p className="text-sm text-gray-500">Market Cap</p>
                  <p className="font-medium">
                    $
                    {AlphaVantageService.formatLargeNumber(
                      overview.MarketCapitalization
                    )}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">P/E Ratio</p>
                  <p className="font-medium">{overview.PERatio}</p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">52 Week Range</p>
                  <p className="font-medium">
                    ${overview["52WeekLow"]} - ${overview["52WeekHigh"]}
                  </p>
                </div>
                <div>
                  <p className="text-sm text-gray-500">Beta</p>
                  <p className="font-medium">{overview.Beta}</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>

        {/* Charts Tab */}
        <TabsContent value="charts">
          <Card>
            <CardHeader>
              <CardTitle>Stock Performance</CardTitle>
            </CardHeader>
            <CardContent className="h-[400px]">
              {stockData && stockData.length > 0 ? (
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={stockData}>
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
              ) : (
                <div className="flex justify-center items-center h-full">
                  <p className="text-gray-500">No price data available</p>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>

        {/* News Tab */}
        <TabsContent value="news">
          <Card>
            <CardHeader>
              <CardTitle>Latest News</CardTitle>
            </CardHeader>
            <CardContent>
              {news && news.length > 0 ? (
                <div className="space-y-6">
                  {news.map((item) => (
                    <div key={item.id} className="border-b last:border-0 pb-4">
                      <h3 className="font-semibold mb-2">{item.title}</h3>
                      <p className="text-gray-600 mb-2">{item.summary}</p>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-500">
                          {item.source}
                        </span>
                        <span className="text-sm text-gray-500">
                          {new Date(item.publishedAt).toLocaleDateString()}
                        </span>
                      </div>
                      <div className="mt-2">
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
                    </div>
                  ))}
                </div>
              ) : (
                <div className="flex justify-center items-center py-8">
                  <p className="text-gray-500">No news available</p>
                </div>
              )}
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default CompanyPage;
