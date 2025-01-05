import { useState, useEffect, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import {
  Search,
  Building2,
  Loader2,
  TrendingUp,
  Globe,
  DollarSign,
  Command,
} from "lucide-react";
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

const REGIONS_MAP: { [key: string]: string } = {
  "United States": "🇺🇸",
  Canada: "🇨🇦",
  "United Kingdom": "🇬🇧",
  Germany: "🇩🇪",
  China: "🇨🇳",
  Japan: "🇯🇵",
};

export const TickerSearch = () => {
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(0);

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
              "Search rate limit reached. Please try again in a minute.",
              {
                icon: "⚠️",
                duration: 4000,
              }
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
          setSelectedIndex(0);
        } else {
          setResults([]);
        }
      } catch (error) {
        console.error("Search error:", error);
        toast.error("Failed to search companies", {
          icon: "❌",
          duration: 3000,
        });
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
    setSearchQuery("");
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
        className="relative w-full cursor-pointer group"
      >
        <Input
          type="text"
          placeholder="Search companies... (Press ⌘K)"
          className="w-full pl-10 pr-12 transition-all group-hover:border-blue-400 group-hover:ring-1 group-hover:ring-blue-200"
          readOnly
        />
        <Search className="absolute left-3 top-2.5 h-5 w-5 text-gray-400 transition-colors group-hover:text-blue-500" />
        <kbd className="absolute right-3 top-2.5 hidden h-5 select-none items-center gap-1 rounded border bg-muted px-1.5 font-mono text-xs text-muted-foreground opacity-100 sm:flex">
          <span className="text-xs">⌘</span>K
        </kbd>
      </div>

      <CommandDialog open={open} onOpenChange={setOpen}>
        <div className="overflow-hidden">
          <DialogTitle className="sr-only">Search companies</DialogTitle>
          <DialogDescription id="dialog-description" className="sr-only">
            Search for companies by name or ticker symbol
          </DialogDescription>

          <div className="flex items-center border-b px-3">
            <Search className="mr-2 h-4 w-4 shrink-0 opacity-50" />
            <CommandInput
              placeholder="Search companies or tickers..."
              value={searchQuery}
              onValueChange={setSearchQuery}
              className="border-none focus:ring-0"
            />
            {searchQuery && !isLoading && (
              <button
                onClick={() => setSearchQuery("")}
                className="ml-2 rounded-sm opacity-50 hover:opacity-100"
              >
                ⌫
              </button>
            )}
          </div>

          <CommandList>
            <CommandEmpty className="py-6 text-center text-sm">
              {isLoading ? (
                <div className="flex flex-col items-center gap-2">
                  <Loader2 className="h-4 w-4 animate-spin" />
                  <span className="text-muted-foreground">
                    Searching markets...
                  </span>
                </div>
              ) : searchQuery ? (
                <div className="flex flex-col items-center gap-2">
                  <Building2 className="h-8 w-8 text-muted-foreground opacity-50" />
                  <span>No companies found</span>
                  <span className="text-xs text-muted-foreground">
                    Try a different search term
                  </span>
                </div>
              ) : (
                <div className="flex flex-col items-center gap-2">
                  <Command className="h-8 w-8 text-muted-foreground opacity-50" />
                  <span>Start typing to search...</span>
                  <div className="flex gap-2 text-xs text-muted-foreground">
                    <kbd className="rounded border bg-muted px-1.5 font-mono">
                      ↑
                    </kbd>
                    <kbd className="rounded border bg-muted px-1.5 font-mono">
                      ↓
                    </kbd>
                    <span>to navigate</span>
                    <kbd className="rounded border bg-muted px-1.5 font-mono">
                      enter
                    </kbd>
                    <span>to select</span>
                  </div>
                </div>
              )}
            </CommandEmpty>

            {!isLoading && results.length > 0 && (
              <CommandGroup heading="Companies">
                {results.map((result, index) => (
                  <CommandItem
                    key={result.symbol}
                    value={result.symbol}
                    onSelect={() => handleSelect(result.symbol)}
                    className={`transition-colors ${
                      index === selectedIndex ? "bg-accent" : ""
                    }`}
                  >
                    <div className="flex w-full items-center justify-between">
                      <div className="flex flex-col">
                        <div className="flex items-center gap-2">
                          <TrendingUp className="h-4 w-4 text-blue-500" />
                          <span className="font-mono font-bold">
                            {result.symbol}
                          </span>
                          <span className="rounded bg-muted px-1.5 py-0.5 text-xs font-medium text-muted-foreground">
                            {result.type}
                          </span>
                        </div>
                        <span className="text-sm text-muted-foreground line-clamp-1">
                          {result.name}
                        </span>
                      </div>
                      <div className="flex items-center gap-2 text-xs text-muted-foreground">
                        <div className="flex items-center gap-1">
                          <Globe className="h-3 w-3" />
                          <span>
                            {REGIONS_MAP[result.region] || result.region}
                          </span>
                        </div>
                        <div className="flex items-center gap-1">
                          <DollarSign className="h-3 w-3" />
                          <span>{result.currency}</span>
                        </div>
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

export default TickerSearch;
