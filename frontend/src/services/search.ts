// src/services/search.ts
export interface CompanySearchResult {
  symbol: string;
  name: string;
  exchange: string;
}

export const searchCompanies = async (query: string): Promise<CompanySearchResult[]> => {
  if (!query.trim()) return [];

  try {
    console.log('Fetching from proxy:', query);
    const response = await fetch(`http://localhost:3001/api/search?query=${encodeURIComponent(query)}`);

    if (!response.ok) {
      console.error('Response not OK:', response.status);
      throw new Error('Failed to fetch');
    }

    const data = await response.json();
    console.log('Received data:', data);

    if (!data?.ResultSet?.Result) {
      console.log('No results found in response');
      return [];
    }

    const results = data.ResultSet.Result.map((result: any) => ({
      symbol: result.symbol,
      name: result.name,
      exchange: result.exch || 'N/A'
    }));

    console.log('Processed results:', results);
    return results;
  } catch (error) {
    console.error('Search error:', error);
    return [];
  }
};