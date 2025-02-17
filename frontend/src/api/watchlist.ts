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

const BASE_URL = "http://localhost:8003/api/v1/watchlist";

// Helper function to get auth headers with debug logging
const getAuthHeaders = () => {
  const token = useAuthStore.getState().token;
  console.log("Raw token value:", token);
  console.log("Full Authorization header:", `Bearer ${token}`);

  if (!token) {
    console.warn("No auth token available in store");
  }

  return {
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
  };
};

export const getWatchlist = async (): Promise<{ items: WatchlistItem[] }> => {
  try {
    const headers = getAuthHeaders();
    console.log('Making request to:', BASE_URL);
    console.log('With headers:', headers);
    
    const response = await axios.get(BASE_URL, headers);
    console.log('Response:', response);
    return response.data;
  } catch (error) {
    if (axios.isAxiosError(error)) {
      // Log the complete error details
      console.log('Error details:', {
        url: error.config?.url,
        method: error.config?.method,
        headers: error.config?.headers,
        data: error.response?.data,
        status: error.response?.status
      });
      
      // Log the response headers
      console.log('Response headers:', error.response?.headers);
    }
    throw error;
  }
};
export const addToWatchlist = async (symbol: string) => {
  try {
    console.debug("Adding to watchlist:", symbol);
    const response = await axios.post(BASE_URL, { symbol }, getAuthHeaders());
    console.debug("Add response:", response.data);
    return response.data;
  } catch (error) {
    console.error("Add to watchlist error:", error);
    throw error;
  }
};

export const removeFromWatchlist = async (symbol: string) => {
  try {
    console.debug("Removing from watchlist:", symbol);
    const response = await axios.delete(
      `${BASE_URL}/${symbol}`,
      getAuthHeaders()
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
    const response = await axios.get(
      `${BASE_URL}/check/${symbol}`,
      getAuthHeaders()
    );
    console.debug("Check status response:", response.data);
    return response.data;
  } catch (error) {
    console.error("Check status error:", error);
    throw error;
  }
};
