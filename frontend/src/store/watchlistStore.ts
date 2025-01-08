import { create } from "zustand";
import * as watchlistAPI from "@/api/watchlist";
import { WatchlistItem } from "@/api/watchlist";

interface WatchlistStore {
  items: WatchlistItem[];
  isLoading: boolean;
  error: string | null;
  fetchWatchlist: () => Promise<void>;
  addToWatchlist: (symbol: string) => Promise<void>;
  removeFromWatchlist: (symbol: string) => Promise<void>;
}

export const useWatchlistStore = create<WatchlistStore>((set, get) => ({
  items: [],
  isLoading: false,
  error: null,

  fetchWatchlist: async () => {
    set({ isLoading: true });
    try {
      const data = await watchlistAPI.getWatchlist();
      set({ items: data.items, error: null });
    } catch (error) {
      set({ error: "Failed to fetch watchlist", items: [] });
    } finally {
      set({ isLoading: false });
    }
  },

  addToWatchlist: async (symbol: string) => {
    try {
      await watchlistAPI.addToWatchlist(symbol);
      await get().fetchWatchlist();
    } catch (error) {
      set({ error: "Failed to add to watchlist" });
    }
  },

  removeFromWatchlist: async (symbol: string) => {
    try {
      await watchlistAPI.removeFromWatchlist(symbol);
      await get().fetchWatchlist();
    } catch (error) {
      set({ error: "Failed to remove from watchlist" });
    }
  },
}));
