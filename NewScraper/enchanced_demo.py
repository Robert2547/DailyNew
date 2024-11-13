"""
Enhanced demo script for testing Financial News Scraper API
Features:
- Interactive menu for different tests
- Status checks for mechanisms
- Detailed performance metrics
- Rich console output
"""
import requests
import json
from datetime import datetime
from typing import Optional, Dict, Any, List
import time
import os
from dotenv import load_dotenv
import logging
import asyncio
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn
from rich.prompt import Prompt, Confirm
from rich.panel import Panel

# Configure logging and rich console
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
console = Console()

# Load environment variables
load_dotenv()

class FinancialNewsAPIClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.api_key = os.getenv("SCRAPEOPS_API_KEY")
        if not self.api_key:
            raise ValueError("SCRAPEOPS_API_KEY not found in environment variables")
        
        self.headers = {
            "X-API-Key": self.api_key,
            "Accept": "application/json"
        }
        
    async def get_news(self, ticker: str) -> Optional[Dict[str, Any]]:
        """Fetch news for a given ticker symbol"""
        try:
            url = f"{self.base_url}/api/v1/news/{ticker}"
            start_time = time.time()
            
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            end_time = time.time()
            data = response.json()
            data['fetch_time'] = end_time - start_time
            
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching news for {ticker}: {str(e)}")
            if hasattr(e.response, 'text'):
                logger.error(f"Response content: {e.response.text}")
            return None

class SystemCheck:
    """Class to check various system mechanisms"""
    def __init__(self):
        self.results = {
            "caching": False,
            "parallel": False
        }
    
    async def check_caching(self, client: FinancialNewsAPIClient):
        """Check if caching is working"""
        try:
            # Make two consecutive requests
            first = await client.get_news("AAPL")
            second = await client.get_news("AAPL")
            
            # Check if second request was faster and from cache
            if (first and second and 
                second['fetch_time'] < first['fetch_time'] and 
                second.get('message') == "Retrieved from cache"):
                self.results["caching"] = True
        except Exception as e:
            logger.error(f"Cache check failed: {e}")
    
    async def check_parallel(self, client: FinancialNewsAPIClient):
        """Check if parallel execution is working"""
        try:
            tickers = ["AAPL", "MSFT", "GOOGL"]
            start_time = time.time()
            results = await asyncio.gather(*[client.get_news(ticker) for ticker in tickers])
            total_time = time.time() - start_time
            
            # If total time is less than sum of individual times, parallel is working
            individual_times = sum(r['fetch_time'] for r in results if r)
            if total_time < individual_times * 0.7:  # 30% faster at least
                self.results["parallel"] = True
        except Exception as e:
            logger.error(f"Parallel check failed: {e}")

    def print_status(self):
        """Print system status"""
        table = Table(title="System Status")
        table.add_column("Mechanism", style="cyan")
        table.add_column("Status", style="bold")
        
        for mechanism, status in self.results.items():
            status_str = "[green]✓ Working" if status else "[red]✗ Not Working"
            table.add_row(mechanism.title(), status_str)
        
        console.print(table)

async def test_single_ticker(client: FinancialNewsAPIClient):
    """Test with a single ticker"""
    ticker = Prompt.ask("Enter ticker symbol", default="AAPL")
    
    with Progress() as progress:
        task = progress.add_task(f"[cyan]Fetching news for {ticker}...", total=None)
        news_data = await client.get_news(ticker)
        progress.update(task, completed=True)
    
    if news_data:
        print_news_data(news_data)

async def test_multiple_tickers(client: FinancialNewsAPIClient):
    """Test with multiple tickers"""
    default_tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]
    tickers_input = Prompt.ask(
        "Enter ticker symbols (comma-separated)",
        default=",".join(default_tickers)
    )
    tickers = [t.strip() for t in tickers_input.split(",")]
    
    with Progress() as progress:
        task = progress.add_task("[cyan]Fetching news...", total=len(tickers))
        results = []
        for ticker in tickers:
            result = await client.get_news(ticker)
            if result:
                results.append(result)
            progress.update(task, advance=1)
    
    for result in results:
        print_news_data(result)
        console.print("\n" + "="*80 + "\n")

def print_news_data(news_data: Dict[str, Any]) -> None:
    """Print news data with statistics"""
    # Source statistics
    stats_table = Table(title=f"News Statistics for {news_data['ticker']}")
    stats_table.add_column("Source", style="cyan")
    stats_table.add_column("Articles", justify="right", style="magenta")
    stats_table.add_column("Fetch Time", justify="right", style="green")
    
    source_stats = {}
    for article in news_data['articles']:
        source = article['source']
        if source not in source_stats:
            source_stats[source] = {'count': 0}
        source_stats[source]['count'] += 1
    
    for source, stats in source_stats.items():
        stats_table.add_row(
            source,
            str(stats['count']),
            f"{news_data['fetch_time']:.2f}s"
        )
    
    console.print(stats_table)
    
    # Articles
    articles_table = Table(title="Articles")
    articles_table.add_column("Source", style="cyan")
    articles_table.add_column("Title", style="white")
    articles_table.add_column("Date", style="green")
    
    for article in news_data['articles']:
        articles_table.add_row(
            article['source'],
            article['title'],
            article['date']
        )
    
    console.print(articles_table)

async def run_system_check(client: FinancialNewsAPIClient) -> SystemCheck:
    """Run system checks"""
    console.print("\n[bold yellow]Running System Checks...[/bold yellow]")
    checker = SystemCheck()
    
    with Progress() as progress:
        task1 = progress.add_task("[cyan]Checking caching...", total=None)
        await checker.check_caching(client)
        progress.update(task1, completed=True)
        
        task2 = progress.add_task("[cyan]Checking parallel execution...", total=None)
        await checker.check_parallel(client)
        progress.update(task2, completed=True)
    
    checker.print_status()
    return checker

async def main_menu():
    """Interactive main menu"""
    client = FinancialNewsAPIClient()
    
    while True:
        console.print("\n[bold cyan]Financial News Scraper Demo[/bold cyan]")
        console.print(Panel.fit(
            "\n".join([
                "[1] Test Single Ticker",
                "[2] Test Multiple Tickers",
                "[3] Run System Check",
                "[4] Exit"
            ]),
            title="Menu Options"
        ))
        
        choice = Prompt.ask("Select an option", choices=["1", "2", "3", "4"])
        
        try:
            if choice == "1":
                await test_single_ticker(client)
            elif choice == "2":
                await test_multiple_tickers(client)
            elif choice == "3":
                checker = await run_system_check(client)
            else:
                console.print("[yellow]Goodbye![/yellow]")
                break
                
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {str(e)}")
        
        if not Confirm.ask("\nWould you like to perform another operation?"):
            break

if __name__ == "__main__":
    try:
        asyncio.run(main_menu())
    except KeyboardInterrupt:
        console.print("\n[yellow]Program terminated by user[/yellow]")
    except Exception as e:
        console.print(f"\n[bold red]Fatal error:[/bold red] {str(e)}")