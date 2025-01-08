import axios from "axios";

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

const BASE_URL = "/api/v1/watchlist";

export const getWatchlist = async (): Promise<{ items: WatchlistItem[] }> => {
  const response = await axios.get(BASE_URL);
  return response.data;
};

export const addToWatchlist = async (symbol: string) => {
  const response = await axios.post(`${BASE_URL}/add/${symbol}`);
  return response.data;
};

export const removeFromWatchlist = async (symbol: string) => {
  const response = await axios.delete(`${BASE_URL}/remove/${symbol}`);
  return response.data;
};

export const checkWatchlistStatus = async (
  symbol: string
): Promise<boolean> => {
  const response = await axios.get(`${BASE_URL}/check/${symbol}`);
  return response.data;
};
