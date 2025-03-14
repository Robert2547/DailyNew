import { create } from "zustand";
import * as watchlistAPI from "@/api/watchlist";
import { WatchlistItem } from "@/api/watchlist";
import { useAuthStore } from "@/store/authStore";

interface WatchlistState {
  items: WatchlistItem[];
  isLoading: boolean;
  error: string | null;
  lastFetchTime: number;
  fetchWatchlist: () => Promise<void>;
  addToWatchlist: (symbol: string) => Promise<void>;
  removeFromWatchlist: (symbol: string) => Promise<void>;
  clearCache: () => void;
}

// Cache time in milliseconds (5 minutes)
const CACHE_TTL = 5 * 60 * 1000;

// Create the store with a reference we can use outside of components
const useWatchlistStore = create<WatchlistState>((set, get) => ({
  items: [],
  isLoading: false,
  error: null,
  lastFetchTime: 0,

  fetchWatchlist: async () => {
    const currentTime = Date.now();
    const lastFetch = get().lastFetchTime;

    // Only fetch if data is stale or doesn't exist
    if (
      get().items.length === 0 ||
      currentTime - lastFetch > CACHE_TTL ||
      get().error !== null
    ) {
      set({ isLoading: true });
      try {
        const token = useAuthStore.getState().token;
        console.debug(
          "Fetching watchlist with token:",
          token ? "Present" : "Missing"
        );

        const data = await watchlistAPI.getWatchlist();
        set({
          items: data.items,
          error: null,
          lastFetchTime: currentTime,
        });
      } catch (error) {
        console.error("Watchlist fetch error:", error);
        set({ error: "Failed to fetch watchlist", items: [] });
      } finally {
        set({ isLoading: false });
      }
    } else {
      console.debug("Using cached watchlist data");
    }
  },

  addToWatchlist: async (symbol: string) => {
    try {
      console.debug("Adding to watchlist:", symbol);
      set((state) => ({
        isLoading: true,
        // Optimistic update
        items: [
          ...state.items,
          {
            id: -1, // Temporary ID
            user_id: -1, // Temporary user ID
            symbol: symbol,
            name: symbol, // Will be updated when fetched
            sector: "",
            price: 0,
            change: 0,
            changePercent: 0,
            marketCap: "",
            added_at: new Date().toISOString(),
          },
        ],
      }));

      await watchlistAPI.addToWatchlist(symbol);
      await get().fetchWatchlist(); // Fetch the updated data
    } catch (error) {
      console.error("Add to watchlist error:", error);
      set({ error: "Failed to add to watchlist" });
      // Roll back optimistic update
      await get().fetchWatchlist();
    } finally {
      set({ isLoading: false });
    }
  },

  removeFromWatchlist: async (symbol: string) => {
    try {
      console.debug("Removing from watchlist:", symbol);

      // Optimistic update
      set((state) => ({
        isLoading: true,
        items: state.items.filter((item) => item.symbol !== symbol),
      }));

      await watchlistAPI.removeFromWatchlist(symbol);
      // No need to fetch again as we've optimistically updated
      set({ lastFetchTime: Date.now() });
    } catch (error) {
      console.error("Remove from watchlist error:", error);
      set({ error: "Failed to remove from watchlist" });
      // Roll back optimistic update
      await get().fetchWatchlist();
    } finally {
      set({ isLoading: false });
    }
  },

  clearCache: () => {
    console.debug("Clearing watchlist cache");
    set({
      items: [],
      isLoading: false,
      error: null,
      lastFetchTime: 0,
    });
  },
}));

// Export a function to clear the cache from outside the component context
export const clearWatchlistCache = () => {
  useWatchlistStore.getState().clearCache();
};

export { useWatchlistStore };
