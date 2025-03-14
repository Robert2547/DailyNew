import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { TrendingUp, TrendingDown, Star, ChevronRight } from "lucide-react";
import { useWatchlistStore } from "@/store/watchlistStore";

interface WatchlistProps {
  limit?: number;
}

export const DashboardWatchlist = ({ limit = 4 }: WatchlistProps) => {
  const navigate = useNavigate();
  const { items = [], isLoading, fetchWatchlist, error } = useWatchlistStore();

  // Fetch watchlist data when component mounts - cached if available
  useEffect(() => {
    let isMounted = true;
    const loadData = async () => {
      try {
        await fetchWatchlist();
      } catch (error) {
        console.error("Failed to load watchlist:", error);
      }
    };

    if (isMounted) {
      loadData();
    }

    return () => {
      isMounted = false;
    };
  }, [fetchWatchlist]);

  const dashboardWatchlist = items.slice(0, limit);

  return (
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
        ) : error ? (
          <div className="text-center py-6">
            <div className="text-red-500 mb-2">Error loading watchlist</div>
            <Button
              variant="outline"
              onClick={() => fetchWatchlist()}
              size="sm"
            >
              Try Again
            </Button>
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
                    <p className="text-sm text-gray-500">
                      {stock.name || "Loading..."}
                    </p>
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
  );
};
