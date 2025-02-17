import { create } from "zustand";
import * as watchlistAPI from "@/api/watchlist";
import { WatchlistItem } from "@/api/watchlist";
import { useAuthStore } from "@/store/authStore";

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
      const token = useAuthStore.getState().token;
      console.debug(
        "Fetching watchlist with token:",
        token ? "Present" : "Missing"
      );

      const data = await watchlistAPI.getWatchlist();
      set({ items: data.items, error: null });
    } catch (error) {
      console.error("Watchlist fetch error:", error);
      set({ error: "Failed to fetch watchlist", items: [] });
    } finally {
      set({ isLoading: false });
    }
  },

  addToWatchlist: async (symbol: string) => {
    try {
      console.debug("Adding to watchlist:", symbol);
      await watchlistAPI.addToWatchlist(symbol);
      await get().fetchWatchlist();
    } catch (error) {
      console.error("Add to watchlist error:", error);
      set({ error: "Failed to add to watchlist" });
    }
  },

  removeFromWatchlist: async (symbol: string) => {
    try {
      console.debug("Removing from watchlist:", symbol);
      await watchlistAPI.removeFromWatchlist(symbol);
      await get().fetchWatchlist();
    } catch (error) {
      console.error("Remove from watchlist error:", error);
      set({ error: "Failed to remove from watchlist" });
    }
  },
}));
