"""
Test script for financial news scraper with interactive menu
"""
import asyncio
from app.services.news_service import NewsService
from app.core.config import settings
from fastapi import BackgroundTasks
import logging
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from typing import List

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
console = Console()

class ScraperTester:
    def __init__(self):
        self.news_service = NewsService()
        # Get scrapers dynamically from news_service
        self.sources = [name for _, name in self.news_service.scrapers]

    async def test_single_ticker(self):
        ticker = Prompt.ask("Enter ticker symbol", default="AAPL")
        background_tasks = BackgroundTasks()
        result = await self.news_service.get_news(ticker, background_tasks)
        print_results(result, self.sources)

    async def test_multiple_tickers(self):
        ticker_input = Prompt.ask("Enter ticker symbols (comma-separated)", default="AAPL,MSFT,GOOGL")
        tickers = [t.strip() for t in ticker_input.split(",")]
        background_tasks = BackgroundTasks()
        
        for ticker in tickers:
            result = await self.news_service.get_news(ticker, background_tasks)
            print_results(result, self.sources)
            console.print("\n" + "="*80 + "\n")

def print_results(news_data, sources):
    if not news_data or not news_data.articles:
        console.print("[red]No data found[/red]")
        return

    # Source statistics
    stats_table = Table(title=f"Source Statistics for {news_data.ticker}")
    stats_table.add_column("Source", style="cyan")
    stats_table.add_column("Articles Found", style="green")
    stats_table.add_column("Status", style="yellow")

    # Initialize counts for all sources
    source_counts = {source: 0 for source in sources}
    for article in news_data.articles:
        source_counts[article.source] += 1

    # Print stats for all sources, even if no articles found
    for source in sources:
        count = source_counts.get(source, 0)
        status = "[green]✓" if count > 0 else "[red]✗"
        stats_table.add_row(source, str(count), status)

    console.print(stats_table)

    # Articles table
    if news_data.articles:
        articles_table = Table(title="Articles Found")
        articles_table.add_column("Source", style="cyan")
        articles_table.add_column("Title", style="white")
        articles_table.add_column("Date", style="green")

        for article in news_data.articles:
            articles_table.add_row(article.source, article.title, article.date)

        console.print(articles_table)

async def main_menu():
    tester = ScraperTester()
    console.print(f"\n[bold cyan]Available News Sources: {', '.join(tester.sources)}[/bold cyan]")

    while True:
        console.print(Panel.fit(
            "\n".join([
                "[1] Test Single Ticker",
                "[2] Test Multiple Tickers",
                "[3] Exit"
            ]),
            title="Menu Options"
        ))
        
        choice = Prompt.ask("Select an option", choices=["1", "2", "3"])
        
        try:
            if choice == "1":
                await tester.test_single_ticker()
            elif choice == "2":
                await tester.test_multiple_tickers()
            else:
                console.print("[yellow]Goodbye![/yellow]")
                break
        except Exception as e:
            console.print(f"[bold red]Error:[/bold red] {str(e)}")
            logger.exception("Error during testing")

        if not Confirm.ask("\nWould you like to perform another test?"):
            break

if __name__ == "__main__":
    try:
        asyncio.run(main_menu())
    except KeyboardInterrupt:
        console.print("\n[yellow]Program terminated by user[/yellow]")
    except Exception as e:
        console.print(f"\n[bold red]Fatal error:[/bold red] {str(e)}")