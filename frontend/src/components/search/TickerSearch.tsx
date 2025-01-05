import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { Search } from "lucide-react";
import {
  CommandDialog,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import { Input } from "@/components/ui/input";
import { DialogTitle, DialogDescription } from "@/components/ui/dialog";
import * as AlphaVantageService from "@/services/alphavantage";
import { useDebounce } from "@/hooks/useDebounce"; 
import toast from "react-hot-toast"; 

interface SearchResult {
  symbol: string;
  name: string;
  type: string;
  region: string;
  currency: string;
  matchScore: number;
}

export const TickerSearch = () => {
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const debouncedSearch = useDebounce(searchQuery, 300);

  const performSearch = useCallback(
    async (query: string) => {
      if (!query.trim()) {
        setResults([]);
        setIsLoading(false);
        return;
      }

      setIsLoading(true);
      try {
        const { data, error } = await AlphaVantageService.searchCompany(
          query.trim()
        );

        if (error) {
          if (error.includes("rate limit")) {
            toast.error(
              "Search rate limit reached. Please try again in a minute."
            );
            navigate("/error", { state: { type: "RATE_LIMIT" } });
            return;
          }
          throw new Error(error);
        }

        if (data) {
          const transformedResults =
            AlphaVantageService.transformSearchResults(data);
          setResults(transformedResults);
        } else {
          setResults([]);
        }
      } catch (error) {
        console.error("Search error:", error);
        toast.error("Failed to search companies");
        setResults([]);
      } finally {
        setIsLoading(false);
      }
    },
    [navigate]
  );

  useEffect(() => {
    performSearch(debouncedSearch);
  }, [debouncedSearch, performSearch]);

  const handleSelect = (symbol: string) => {
    setOpen(false);
    navigate(`/company/${symbol}`);
  };

  useEffect(() => {
    const down = (e: KeyboardEvent) => {
      if (e.key === "k" && (e.metaKey || e.ctrlKey)) {
        e.preventDefault();
        setOpen((open) => !open);
      }
    };

    document.addEventListener("keydown", down);
    return () => document.removeEventListener("keydown", down);
  }, []);

  return (
    <>
      <div
        onClick={() => setOpen(true)}
        className="relative w-full cursor-pointer"
      >
        <Input
          type="text"
          placeholder="Search companies... (Press ⌘K)"
          className="w-full pl-10"
          readOnly
        />
        <Search className="absolute left-3 top-2.5 h-5 w-5 text-gray-400" />
      </div>

      <CommandDialog open={open} onOpenChange={setOpen}>
        <div>
          <DialogTitle className="sr-only">Search companies</DialogTitle>
          <DialogDescription id="dialog-description" className="sr-only">
            Search for companies by name or ticker symbol
          </DialogDescription>
          <CommandInput
            placeholder="Search companies or tickers..."
            value={searchQuery}
            onValueChange={setSearchQuery}
            className="border-none focus:ring-0"
          />

          <CommandList>
            <CommandEmpty className="py-6 text-center text-sm">
              {isLoading ? "Searching..." : "No companies found"}
            </CommandEmpty>

            {!isLoading && results.length > 0 && (
              <CommandGroup>
                {results.map((result) => (
                  <CommandItem
                    key={result.symbol}
                    value={result.symbol}
                    onSelect={() => handleSelect(result.symbol)}
                  >
                    <div className="flex flex-col">
                      <div className="flex items-center">
                        <span className="font-medium">{result.symbol}</span>
                        <span className="ml-2 text-xs text-gray-500">
                          {result.region} · {result.currency}
                        </span>
                      </div>
                      <div className="text-sm text-muted-foreground">
                        {result.name}
                      </div>
                    </div>
                  </CommandItem>
                ))}
              </CommandGroup>
            )}
          </CommandList>
        </div>
      </CommandDialog>
    </>
  );
};
