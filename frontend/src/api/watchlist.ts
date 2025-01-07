import axios from "axios";

const BASE_URL = "/api/watchlist";

export const getWatchlist = async () => {
  const response = await axios.get(BASE_URL);
  return response.data;
};

export const addToWatchlist = async (symbol: string) => {
  const response = await axios.post(`${BASE_URL}/add`, { symbol });
  return response.data;
};

export const removeFromWatchlist = async (symbol: string) => {
  const response = await axios.delete(`${BASE_URL}/remove/${symbol}`);
  return response.data;
};

export const checkWatchlistStatus = async (symbol: string) => {
  const response = await axios.get(`${BASE_URL}/check/${symbol}`);
  return response.data;
};
