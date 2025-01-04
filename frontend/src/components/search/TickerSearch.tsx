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
import { searchCompanies } from "@/services/search";
import type { CompanySearchResult } from "@/types/index";

export const TickerSearch = () => {
  const navigate = useNavigate();
  const [open, setOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [results, setResults] = useState<CompanySearchResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  const performSearch = useCallback(async (query: string) => {
    if (!query.trim()) {
      setResults([]);
      setIsLoading(false);
      return;
    }

    setIsLoading(true);
    try {
      const searchResults = await searchCompanies(query.trim());
      console.log("Search results:", searchResults); // Debug log
      setResults(searchResults);
    } catch (error) {
      console.error("Search error:", error);
      setResults([]);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => {
      performSearch(searchQuery);
    }, 300);

    return () => clearTimeout(timer);
  }, [searchQuery, performSearch]);

  const handleSelect = (symbol: string) => {
    setOpen(false);
    navigate(`/company/${symbol}`);
  };

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
                      <div className="font-medium">{result.symbol}</div>
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
