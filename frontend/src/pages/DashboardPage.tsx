import {
  TrendingUp,
  TrendingDown,
  Eye,
  Newspaper,
  BarChart2,
  ExternalLink,
  Star,
  ChevronRight,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";
import { useWatchlistStore } from "@/store/watchlistStore";
import { useEffect } from "react";
import { useAuthStore } from "@/store/authStore";

const mockNews = [
  {
    id: 1,
    title: "Federal Reserve Holds Interest Rates Steady",
    source: "Financial Times",
    sentiment: "neutral",
    time: "2h ago",
  },
  {
    id: 2,
    title: "Apple's AI Strategy Shows Promise, Analysts Say",
    source: "Bloomberg",
    sentiment: "positive",
    time: "4h ago",
  },
  {
    id: 3,
    title: "Tech Sector Faces New Regulatory Challenges",
    source: "Reuters",
    sentiment: "negative",
    time: "5h ago",
  },
];

const StatsCard = ({ title, value, trend, icon: Icon, trendColor }: any) => (
  <Card>
    <CardHeader className="flex flex-row items-center justify-between pb-2">
      <CardTitle className="text-sm font-medium text-gray-500">
        {title}
      </CardTitle>
      <Icon className={`h-4 w-4 ${trendColor}`} />
    </CardHeader>
    <CardContent>
      <div className="text-2xl font-bold">{value}</div>
      <p className={`text-sm ${trendColor} flex items-center mt-1`}>
        {trend > 0 ? (
          <TrendingUp className="h-4 w-4 mr-1" />
        ) : (
          <TrendingDown className="h-4 w-4 mr-1" />
        )}
        {trend > 0 ? "+" : ""}
        {trend}% from yesterday
      </p>
    </CardContent>
  </Card>
);

export const DashboardPage = () => {
  const navigate = useNavigate();
  const { items = [], isLoading, fetchWatchlist } = useWatchlistStore();
  const { user } = useAuthStore();

  // Fetch watchlist data when component mounts
  useEffect(() => {
    fetchWatchlist();
  }, [fetchWatchlist]);

  const stats = [
    {
      title: "Tracked Companies",
      value: "12",
      trend: 2,
      icon: Eye,
      trendColor: "text-green-500",
    },
    {
      title: "Today's News",
      value: "89",
      trend: 14,
      icon: Newspaper,
      trendColor: "text-green-500",
    },
    {
      title: "Market Sentiment",
      value: "70%",
      trend: -5,
      icon: BarChart2,
      trendColor: "text-red-500",
    },
  ];

  const dashboardWatchlist = items.slice(0, 4);

  return (
    <>
      {/* Welcome Banner remains the same */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-400 rounded-lg shadow-lg p-6 mb-8 text-white">
        <h1 className="text-3xl font-bold">Welcome back, {user?.email || "User!"} 👋</h1>
        <p className="mt-2 text-blue-50">
          Here's what's happening with your watched companies today
        </p>
      </div>

      {/* Stats Grid remains the same */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {stats.map((stat, index) => (
          <StatsCard key={index} {...stat} />
        ))}
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Watchlist */}
        <Card className="md:col-span-2">
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <Star className="h-5 w-5 text-yellow-500" />
              Watchlist
            </CardTitle>
            <Button
              variant="ghost"
              size="sm"
              className="text-blue-600"
              onClick={() => navigate("/watchlist")}
            >
              View All
              <ChevronRight className="ml-1 h-4 w-4" />
            </Button>
          </CardHeader>
          <CardContent>
            {isLoading ? (
              <div className="flex justify-center items-center py-8">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900" />
              </div>
            ) : dashboardWatchlist.length === 0 ? (
              <div className="text-center py-8">
                <Star className="h-12 w-12 text-gray-300 mx-auto mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-1">
                  No stocks in your watchlist
                </h3>
                <p className="text-gray-500">
                  Start by adding some stocks to track their performance
                </p>
                <Button
                  variant="outline"
                  className="mt-4"
                  onClick={() => navigate("/watchlist")}
                >
                  Go to Watchlist
                </Button>
              </div>
            ) : (
              <div className="space-y-4">
                {dashboardWatchlist.map((stock) => (
                  <div
                    key={stock.symbol}
                    className="flex items-center justify-between p-3 hover:bg-gray-50 rounded-lg transition-colors cursor-pointer"
                    onClick={() => navigate(`/company/${stock.symbol}`)}
                  >
                    <div className="flex items-center gap-4">
                      <div className="w-10 h-10 bg-blue-100 rounded-full flex items-center justify-center">
                        <span className="font-mono font-bold text-blue-600">
                          {stock.symbol?.slice(0, 2)}
                        </span>
                      </div>
                      <div>
                        <h3 className="font-medium">{stock.symbol}</h3>
                        <p className="text-sm text-gray-500">{stock.name}</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="font-mono font-medium">
                        $
                        {typeof stock.price === "number"
                          ? stock.price.toFixed(2)
                          : "N/A"}
                      </div>
                      <div
                        className={`text-sm flex items-center justify-end ${
                          (stock.change || 0) >= 0
                            ? "text-green-600"
                            : "text-red-600"
                        }`}
                      >
                        {(stock.change || 0) >= 0 ? (
                          <TrendingUp className="h-3 w-3 mr-1" />
                        ) : (
                          <TrendingDown className="h-3 w-3 mr-1" />
                        )}
                        {typeof stock.changePercent === "number" ? (
                          <>
                            {stock.changePercent > 0 ? "+" : ""}
                            {stock.changePercent.toFixed(2)}%
                          </>
                        ) : (
                          "N/A"
                        )}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </CardContent>
        </Card>
        {/* News Feed */}
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <Newspaper className="h-5 w-5 text-blue-500" />
              Latest News
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {mockNews.map((item) => (
                <div
                  key={item.id}
                  className="group flex flex-col gap-2 p-3 hover:bg-gray-50 rounded-lg transition-colors"
                >
                  <div className="flex items-center justify-between">
                    <span
                      className={`text-xs px-2 py-1 rounded-full ${
                        item.sentiment === "positive"
                          ? "bg-green-100 text-green-800"
                          : item.sentiment === "negative"
                          ? "bg-red-100 text-red-800"
                          : "bg-gray-100 text-gray-800"
                      }`}
                    >
                      {item.sentiment}
                    </span>
                    <div className="text-xs text-gray-500">{item.time}</div>
                  </div>
                  <h3 className="font-medium text-sm group-hover:text-blue-600 transition-colors">
                    {item.title}
                  </h3>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-gray-500">{item.source}</span>
                    <ExternalLink className="h-3 w-3 text-gray-400 group-hover:text-blue-500 transition-colors" />
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </>
  );
};

export default DashboardPage;
