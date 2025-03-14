import axios from "axios";
import { useAuthStore } from "@/store/authStore";

export interface WatchlistItem {
  id: number;
  user_id: number;
  symbol: string;
  name: string;
  sector: string;
  price: number;
  change: number;
  changePercent: number;
  marketCap: string;
  added_at: string;
}

const BASE_URL = "http://127.0.0.1:8003/api/v1/watchlist";

// Add request tracking and retry mechanism
let pendingRequests = 0;
const MAX_RETRIES = 2;
const RETRY_DELAY = 1000; // 1 second

// Helper function to get auth headers with debug logging
const getAuthHeaders = () => {
  const token = useAuthStore.getState().token;

  if (!token) {
    console.warn("No auth token available in store");
    throw new Error("Authentication token is missing");
  }

  return {
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  };
};

// Helper function to handle retries
const withRetry = async <T>(
  requestFn: () => Promise<T>,
  retries = MAX_RETRIES
): Promise<T> => {
  try {
    pendingRequests++;
    return await requestFn();
  } catch (error) {
    if (retries > 0 && axios.isAxiosError(error)) {
      // Only retry on network errors or 5xx server errors
      if (!error.response || error.response.status >= 500) {
        console.log(
          `Retrying request (${MAX_RETRIES - retries + 1}/${MAX_RETRIES})...`
        );
        await new Promise((resolve) => setTimeout(resolve, RETRY_DELAY));
        return withRetry(requestFn, retries - 1);
      }
    }
    throw error;
  } finally {
    pendingRequests--;
  }
};

export const getWatchlist = async (): Promise<{ items: WatchlistItem[] }> => {
  try {
    const headers = getAuthHeaders();

    // Check if we already have pending requests
    if (pendingRequests > 0) {
      console.log("There's already a pending watchlist request, waiting...");
      await new Promise((resolve) => setTimeout(resolve, 200));
    }

    const response = await withRetry(() => axios.get(BASE_URL, headers));
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      // Log the complete error details
      console.log("Error details:", {
        url: error.config?.url,
        method: error.config?.method,
        headers: error.config?.headers,
        data: error.response?.data,
        status: error.response?.status,
      });

      // Authentication errors
      if (error.response?.status === 401 || error.response?.status === 403) {
        console.error("Authentication failed when fetching watchlist");
        // Could trigger logout here for invalid token
      }
    }
    throw error;
  }
};

export const addToWatchlist = async (symbol: string) => {
  try {
    console.debug("Adding to watchlist:", symbol);
    const response = await withRetry(() =>
      axios.post(BASE_URL, { symbol }, getAuthHeaders())
    );
    console.debug("Add response:", response.data);
    return response.data;
  } catch (error) {
    console.error("Add to watchlist error:", error);
    // Check for duplicate entry error
    if (axios.isAxiosError(error) && error.response?.status === 409) {
      console.log("Stock is already in watchlist");
      return { status: "already_exists" };
    }
    throw error;
  }
};

export const removeFromWatchlist = async (symbol: string) => {
  try {
    console.debug("Removing from watchlist:", symbol);
    const response = await withRetry(() =>
      axios.delete(`${BASE_URL}/${symbol}`, getAuthHeaders())
    );
    console.debug("Remove response:", response.data);
    return response.data;
  } catch (error) {
    console.error("Remove from watchlist error:", error);
    throw error;
  }
};

export const checkWatchlistStatus = async (
  symbol: string
): Promise<boolean> => {
  try {
    console.debug("Checking watchlist status for:", symbol);
    const response = await withRetry(() =>
      axios.get(`${BASE_URL}/check/${symbol}`, getAuthHeaders())
    );
    console.debug("Check status response:", response.data);
    return response.data;
  } catch (error) {
    console.error("Check status error:", error);
    // If we get a 404, it means the stock is not in the watchlist
    if (axios.isAxiosError(error) && error.response?.status === 404) {
      return false;
    }
    throw error;
  }
};
