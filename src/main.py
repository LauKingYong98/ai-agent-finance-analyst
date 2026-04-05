"""CLI entry point for the AI Agent Finance Analyst.

Usage:
    python -m src.main analyze AAPL
    python -m src.main analyze AAPL --verbose
"""

import asyncio
import json
import sys

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from src.orchestrator import AnalysisPipeline

console = Console()


def display_thesis(thesis: dict):
    """Display the final thesis in a rich formatted output."""
    ticker = thesis.get("ticker", "???")
    rec = thesis.get("recommendation", "N/A")
    conviction = thesis.get("conviction", "N/A")
    current = thesis.get("current_price", "N/A")
    target = thesis.get("target_price", {})

    # Color the recommendation
    rec_color = {"BUY": "green", "HOLD": "yellow", "SELL": "red"}.get(rec, "white")

    console.print()
    console.print(Panel(
        f"[bold]{ticker}[/bold] Investment Thesis",
        style="bold blue",
    ))

    # Recommendation table
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column("Label", style="dim")
    table.add_column("Value", style="bold")
    table.add_row("Recommendation", f"[{rec_color}]{rec}[/{rec_color}]")
    table.add_row("Conviction", f"{conviction}/10")
    table.add_row("Current Price", f"${current}")
    table.add_row("Target (Bull)", f"${target.get('bull', 'N/A')}")
    table.add_row("Target (Base)", f"${target.get('base', 'N/A')}")
    table.add_row("Target (Bear)", f"${target.get('bear', 'N/A')}")
    table.add_row("Time Horizon", thesis.get("time_horizon", "12 months"))
    console.print(table)

    # Executive summary
    if "executive_summary" in thesis:
        console.print()
        console.print(Panel(thesis["executive_summary"], title="Executive Summary", border_style="blue"))

    # Key catalysts
    catalysts = thesis.get("key_catalysts", [])
    if catalysts:
        console.print()
        console.print("[bold]Key Catalysts:[/bold]")
        for c in catalysts:
            console.print(f"  [green]+[/green] {c}")

    # Key risks
    risks = thesis.get("key_risks", [])
    if risks:
        console.print()
        console.print("[bold]Key Risks:[/bold]")
        for r in risks:
            console.print(f"  [red]-[/red] {r}")

    # Red team summary
    rt = thesis.get("red_team_summary", {})
    if rt.get("strongest_challenge"):
        console.print()
        console.print(Panel(
            f"[bold]Strongest Challenge:[/bold] {rt['strongest_challenge']}\n\n"
            f"[bold]Thesis Adjustment:[/bold] {rt.get('thesis_adjustment', 'N/A')}",
            title="Red Team Review",
            border_style="red",
        ))

    console.print()


@click.group()
def cli():
    """AI Agent Finance Analyst — Multi-agent investment analysis powered by Claude."""
    pass


@cli.command()
@click.argument("ticker")
@click.option("--verbose", "-v", is_flag=True, help="Enable verbose logging")
@click.option("--output", "-o", type=click.Path(), help="Custom output path for final thesis JSON")
def analyze(ticker: str, verbose: bool, output: str | None):
    """Run full investment analysis for a stock ticker.

    Example: python -m src.main analyze AAPL
    """
    console.print(f"\n[bold blue]AI Agent Finance Analyst[/bold blue]")
    console.print(f"Analyzing [bold]{ticker.upper()}[/bold]...\n")

    pipeline = AnalysisPipeline(ticker, verbose=verbose)

    try:
        final_thesis = asyncio.run(pipeline.run())
    except KeyboardInterrupt:
        console.print("\n[yellow]Analysis interrupted by user.[/yellow]")
        sys.exit(1)
    except Exception as e:
        console.print(f"\n[red]Error during analysis: {e}[/red]")
        if verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

    # Display results
    display_thesis(final_thesis)

    # Save to custom output path if specified
    if output:
        with open(output, "w") as f:
            json.dump(final_thesis, f, indent=2)
        console.print(f"[dim]Thesis saved to {output}[/dim]")

    console.print(f"[dim]All reports saved to workspace/analysis/{ticker.upper()}/[/dim]\n")


@cli.command()
@click.argument("ticker")
def view(ticker: str):
    """View a previously generated thesis.

    Example: python -m src.main view AAPL
    """
    path = f"workspace/analysis/{ticker.upper()}/thesis_final_report.json"
    try:
        with open(path) as f:
            thesis = json.load(f)
        display_thesis(thesis)
    except FileNotFoundError:
        console.print(f"[red]No thesis found for {ticker.upper()}. Run 'analyze' first.[/red]")
        sys.exit(1)


if __name__ == "__main__":
    cli()
