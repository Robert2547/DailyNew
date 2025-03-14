import { useEffect, useState } from "react";
import {
  TrendingUp,
  TrendingDown,
  Eye,
  Newspaper,
  BarChart2,
  ExternalLink,
} from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { useNavigate } from "react-router-dom";
import { useAuthStore } from "@/store/authStore";
import { useWatchlistStore } from "@/store/watchlistStore";
import { DashboardWatchlist } from "@/components/dashboard/watchlist";

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

interface StatsCardProps {
  title: string;
  value: string | number;
  trend: number;
  icon: React.ElementType;
  trendColor: string;
}

const StatsCard = ({
  title,
  value,
  trend,
  icon: Icon,
  trendColor,
}: StatsCardProps) => (
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

// Count news items from the last 24 hours
const countRecentNews = (news: any[]) => {
  const oneDayAgo = new Date();
  oneDayAgo.setHours(oneDayAgo.getHours() - 24);

  return news.filter((item) => {
    const timeText = item.time;
    if (timeText.includes("h ago")) {
      const hours = parseInt(timeText);
      return hours <= 24;
    }
    return false;
  }).length;
};

export const DashboardPage = () => {
  const navigate = useNavigate();
  const { user } = useAuthStore();
  const { items = [], fetchWatchlist } = useWatchlistStore();
  const [recentNewsCount, setRecentNewsCount] = useState(0);

  // Fetch watchlist on component mount
  useEffect(() => {
    fetchWatchlist();

    // Count recent news
    // TODO: fetch the actual news timestamps
    setRecentNewsCount(countRecentNews(mockNews));
  }, [fetchWatchlist]);

  // Calculate the previous count for trend
  const previousWatchlistCount = Math.max(
    1,
    items.length - Math.ceil(items.length * 0.1)
  );
  const watchlistTrend =
    items.length > 0
      ? Math.round(
          ((items.length - previousWatchlistCount) / previousWatchlistCount) *
            100
        )
      : 0;

  const previousNewsCount = Math.max(1, recentNewsCount - 1);
  const newsTrend =
    recentNewsCount > 0
      ? Math.round(
          ((recentNewsCount - previousNewsCount) / previousNewsCount) * 100
        )
      : 0;

  const stats = [
    {
      title: "Tracked Companies",
      value: items.length,
      trend: watchlistTrend,
      icon: Eye,
      trendColor: watchlistTrend >= 0 ? "text-green-500" : "text-red-500",
    },
    {
      title: "Today's News",
      value: recentNewsCount,
      trend: newsTrend,
      icon: Newspaper,
      trendColor: newsTrend >= 0 ? "text-green-500" : "text-red-500",
    },
    {
      title: "Market Sentiment",
      value: "70%",
      trend: -5,
      icon: BarChart2,
      trendColor: "text-red-500",
    },
  ];

  return (
    <>
      {/* Welcome Banner */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-400 rounded-lg shadow-lg p-6 mb-8 text-white">
        <h1 className="text-3xl font-bold">
          Welcome back, {user?.email || "User!"} 👋
        </h1>
        <p className="mt-2 text-blue-50">
          Here's what's happening with your watched companies today
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        {stats.map((stat, index) => (
          <StatsCard key={index} {...stat} />
        ))}
      </div>

      {/* Main Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Use the extracted watchlist component */}
        <DashboardWatchlist limit={4} />

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
