import { useState, useEffect, useCallback } from "react"; // Add useCallback
import {
  TrendingUp,
  TrendingDown,
  ArrowLeft,
  Star,
  Trash2,
  Search,
} from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogFooter,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { useNavigate } from "react-router-dom";
import { useWatchlistStore } from "@/store/watchlistStore";

export const WatchlistPage = () => {
  const navigate = useNavigate();
  const [searchQuery, setSearchQuery] = useState("");
  const {
    items = [],
    isLoading,
    fetchWatchlist,
    removeFromWatchlist,
  } = useWatchlistStore();

  const [deleteDialog, setDeleteDialog] = useState({
    isOpen: false,
    stockSymbol: "",
    stockName: "",
  });

  // Wrap fetchWatchlist in useCallback
  const fetchWatchlistData = useCallback(() => {
    fetchWatchlist();
  }, [fetchWatchlist]);

  useEffect(() => {
    fetchWatchlistData();
  }, [fetchWatchlistData]);

  const handleRemoveStock = async (symbol: string) => {
    try {
      await removeFromWatchlist(symbol);
      setDeleteDialog({ isOpen: false, stockSymbol: "", stockName: "" });
    } catch (error) {
      console.error("Failed to remove stock:", error);
    }
  };

  const openDeleteDialog = (symbol: string, name: string) => {
    setDeleteDialog({
      isOpen: true,
      stockSymbol: symbol,
      stockName: name,
    });
  };

  const handleStockClick = (symbol: string) => {
    navigate(`/company/${symbol}`);
  };

  // Add safety check for items
  const filteredStocks = (items || []).filter(
    (stock) =>
      stock.symbol.toLowerCase().includes(searchQuery.toLowerCase()) ||
      stock.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900" />
      </div>
    );
  }
  return (
    <div className="max-w-5xl mx-auto px-4 py-8">
      {/* Header */}
      <div className="flex flex-col gap-6 mb-8">
        <div className="flex items-center gap-2">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => navigate("/dashboard")}
            className="text-gray-600 hover:text-gray-900"
          >
            <ArrowLeft className="h-4 w-4 mr-2" />
            Back to Dashboard
          </Button>
        </div>

        <div className="flex flex-col gap-2">
          <h1 className="text-3xl font-bold flex items-center gap-2">
            <Star className="h-7 w-7 text-yellow-500" />
            Watchlist
          </h1>
          <p className="text-gray-500">
            Track and monitor your favorite stocks in one place
          </p>
        </div>

        {/* Search  Bar */}
        <div className="flex gap-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-2.5 h-5 w-5 text-gray-400" />
            <Input
              placeholder="Search stocks..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10"
            />
          </div>
        </div>
      </div>

      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <div>
              <CardTitle>Your Stocks ({filteredStocks.length})</CardTitle>
              <CardDescription>
                Click on a stock to view detailed information
              </CardDescription>
            </div>
            {searchQuery && filteredStocks.length === 0 && (
              <p className="text-gray-500">No matching stocks found</p>
            )}
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            {filteredStocks.length === 0 && !searchQuery ? (
              <div className="text-center py-12">
                <div className="flex justify-center mb-4">
                  <Star className="h-12 w-12 text-gray-300" />
                </div>
                <h3 className="text-lg font-medium text-gray-900 mb-1">
                  No stocks in your watchlist
                </h3>
                <p className="text-gray-500">
                  Start by adding some stocks to track their performance
                </p>
              </div>
            ) : (
              filteredStocks.map((stock) => (
                <div
                  key={stock.symbol}
                  className="flex items-center justify-between p-4 hover:bg-gray-50 rounded-lg transition-colors border"
                >
                  <div
                    className="flex items-center gap-4 flex-1 cursor-pointer"
                    onClick={() => handleStockClick(stock.symbol)}
                  >
                    <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl flex items-center justify-center text-white">
                      <span className="font-mono font-bold">
                        {stock.symbol.slice(0, 2)}
                      </span>
                    </div>
                    <div>
                      <div className="flex items-center gap-2">
                        <h3 className="font-medium text-lg">{stock.symbol}</h3>
                        <span className="text-xs px-2 py-1 bg-gray-100 rounded-full text-gray-600">
                          {stock.sector}
                        </span>
                      </div>
                      <div className="flex items-center gap-3">
                        <p className="text-gray-500">{stock.name}</p>
                        <span className="text-xs text-gray-400">•</span>
                        <p className="text-sm text-gray-400">
                          MC: {stock.marketCap}
                        </p>
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-8">
                    <div className="text-right min-w-[120px]">
                      <div className="font-mono font-medium text-lg">
                        $
                        {typeof stock.price === "number"
                          ? stock.price.toFixed(2)
                          : "N/A"}
                      </div>
                      <div
                        className={`text-sm flex items-center justify-end font-medium ${
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
                    <Button
                      variant="ghost"
                      size="sm"
                      className="text-gray-400 hover:text-red-600 hover:bg-red-50"
                      onClick={() => openDeleteDialog(stock.symbol, stock.name)}
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              ))
            )}
          </div>
        </CardContent>
      </Card>

      {/* Confirm Delete Stock Waitlist Dialog */}
      <Dialog
        open={deleteDialog.isOpen}
        onOpenChange={(open) =>
          !open && setDeleteDialog((prev) => ({ ...prev, isOpen: false }))
        }
      >
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Remove Stock from Watchlist</DialogTitle>
            <DialogDescription>
              Are you sure you want to remove {deleteDialog.stockSymbol} from your watchlist? This action cannot
              be undone.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter className="flex gap-2 justify-end mt-4">
            <Button
              variant="outline"
              onClick={() =>
                setDeleteDialog({
                  isOpen: false,
                  stockSymbol: "",
                  stockName: "",
                })
              }
            >
              Cancel
            </Button>
            <Button
              variant="destructive"
              onClick={() => handleRemoveStock(deleteDialog.stockSymbol)}
            >
              Remove
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default WatchlistPage;
