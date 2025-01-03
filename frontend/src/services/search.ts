const ALPHA_VANTAGE_API_KEY = import.meta.env.VITE_ALPHA_VANTAGE_API_KEY;

import type { CompanySearchResult } from "../types";

export const searchCompanies = async (
  query: string
): Promise<CompanySearchResult[]> => {
  console.log("Searching for:", query);
  console.log("Using API key:", ALPHA_VANTAGE_API_KEY); // Make sure to remove this in production

  if (!query.trim()) return [];

  try {
    const url = `https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=${encodeURIComponent(
      query
    )}&apikey=${ALPHA_VANTAGE_API_KEY}`;
    console.log("Fetching from URL:", url);

    const response = await fetch(url);
    console.log("Response status:", response.status);

    const data = await response.json();
    console.log("API Response:", data);

    if (!response.ok) {
      throw new Error(`API error: ${response.status}`);
    }

    if (!data.bestMatches) {
      console.log("No matches found in response");
      return [];
    }

    const results = data.bestMatches.map((match: any) => ({
      symbol: match["1. symbol"],
      name: match["2. name"],
      type: match["3. type"],
      region: match["4. region"],
    }));

    console.log("Processed results:", results);
    return results;
  } catch (error) {
    console.error("Error searching companies:", error);
    return [];
  }
};
