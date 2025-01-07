import { create } from "zustand";
import * as watchlistAPI from "@/api/watchlist";

interface WatchlistStore {
  stocks: WatchlistStock[];
  isLoading: boolean;
  error: string | null;
  fetchWatchlist: () => Promise<void>;
  addStock: (symbol: string) => Promise<void>;
  removeStock: (symbol: string) => Promise<void>;
}

interface WatchlistStock {
  symbol: string;
  name: string;
  price: number;
  change: number;
  changePercent: number;
  sector: string;
  marketCap: string;
}

export const useWatchlistStore = create<WatchlistStore>((set, get) => ({
  stocks: [],
  isLoading: false,
  error: null,

  fetchWatchlist: async () => {
    set({ isLoading: true });
    try {
      const data = await watchlistAPI.getWatchlist();
      set({ stocks: data, error: null });
    } catch (error) {
      set({ error: "Failed to fetch watchlist" });
    } finally {
      set({ isLoading: false });
    }
  },

  addStock: async (symbol) => {
    try {
      await watchlistAPI.addToWatchlist(symbol);
      await get().fetchWatchlist();
    } catch (error) {
      set({ error: "Failed to add stock to watchlist" });
    }
  },

  removeStock: async (symbol) => {
    try {
      await watchlistAPI.removeFromWatchlist(symbol);
      await get().fetchWatchlist();
    } catch (error) {
      set({ error: "Failed to remove stock from watchlist" });
    }
  },
}));
