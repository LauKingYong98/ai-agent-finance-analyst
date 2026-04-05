#!/usr/bin/env python3
"""Comparable company analysis.

Usage:
    python -m src.scripts.comparables AAPL [--peers MSFT,GOOGL,META,AMZN]

Output: JSON to stdout with comparable analysis results.
"""

import argparse
import json
import sys

import numpy as np
import yfinance as yf


def get_valuation_metrics(ticker: str) -> dict | None:
    """Fetch valuation metrics for a single ticker."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        ev = info.get("enterpriseValue", 0)
        ebitda = info.get("ebitda", 0)
        pe = info.get("trailingPE")
        forward_pe = info.get("forwardPE")
        peg = info.get("pegRatio")
        market_cap = info.get("marketCap", 0)
        revenue = info.get("totalRevenue", 0)
        earnings_growth = info.get("earningsGrowth")
        revenue_growth = info.get("revenueGrowth")
        current_price = info.get("currentPrice", info.get("regularMarketPrice", 0))

        ev_ebitda = round(ev / ebitda, 2) if ebitda and ebitda > 0 else None
        ev_revenue = round(ev / revenue, 2) if revenue and revenue > 0 else None

        return {
            "ticker": ticker,
            "current_price": current_price,
            "market_cap": market_cap,
            "enterprise_value": ev,
            "ev_ebitda": ev_ebitda,
            "ev_revenue": ev_revenue,
            "pe_trailing": round(pe, 2) if pe else None,
            "pe_forward": round(forward_pe, 2) if forward_pe else None,
            "peg_ratio": round(peg, 2) if peg else None,
            "earnings_growth": round(earnings_growth, 4) if earnings_growth else None,
            "revenue_growth": round(revenue_growth, 4) if revenue_growth else None,
        }
    except Exception as e:
        return {"ticker": ticker, "error": str(e)}


def auto_select_peers(ticker: str, max_peers: int = 5) -> list[str]:
    """Attempt to auto-select peers based on sector and industry."""
    stock = yf.Ticker(ticker)
    info = stock.info
    sector = info.get("sector", "")
    industry = info.get("industry", "")

    # Common peer mappings for well-known sectors
    tech_mega = {"AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA"}
    if ticker.upper() in tech_mega:
        peers = list(tech_mega - {ticker.upper()})
        return peers[:max_peers]

    # Fallback: return empty and let the agent provide peers
    return []


def run_comparables(ticker: str, peers: list[str] | None = None) -> dict:
    """Run comparable company analysis."""
    if not peers:
        peers = auto_select_peers(ticker)
        if not peers:
            return {
                "ticker": ticker,
                "error": "No peers provided and auto-selection failed. Please provide --peers.",
            }

    subject = get_valuation_metrics(ticker)
    peer_metrics = [get_valuation_metrics(p) for p in peers]

    # Filter out peers with errors
    valid_peers = [p for p in peer_metrics if "error" not in p]

    if not valid_peers:
        return {"ticker": ticker, "error": "Failed to fetch metrics for all peers"}

    # Compute peer medians
    def safe_median(values):
        clean = [v for v in values if v is not None]
        return round(float(np.median(clean)), 2) if clean else None

    peer_ev_ebitda = safe_median([p["ev_ebitda"] for p in valid_peers])
    peer_pe = safe_median([p["pe_trailing"] for p in valid_peers])
    peer_ev_revenue = safe_median([p["ev_revenue"] for p in valid_peers])
    peer_peg = safe_median([p["peg_ratio"] for p in valid_peers])

    # Compute implied prices from peer multiples
    subject_info = yf.Ticker(ticker).info
    shares = subject_info.get("sharesOutstanding", 1)
    ebitda = subject_info.get("ebitda", 0)
    eps = subject_info.get("trailingEps", 0)
    revenue = subject_info.get("totalRevenue", 0)
    total_debt = subject_info.get("totalDebt", 0)
    cash = subject_info.get("totalCash", 0)

    implied_price_ev_ebitda = None
    if peer_ev_ebitda and ebitda and ebitda > 0 and shares > 0:
        implied_ev = peer_ev_ebitda * ebitda
        implied_equity = implied_ev - total_debt + cash
        implied_price_ev_ebitda = round(implied_equity / shares, 2)

    implied_price_pe = None
    if peer_pe and eps and eps > 0:
        implied_price_pe = round(peer_pe * eps, 2)

    # Relative valuation assessment
    current_price = subject.get("current_price", 0) if subject else 0
    if implied_price_ev_ebitda and implied_price_pe and current_price > 0:
        avg_implied = (implied_price_ev_ebitda + implied_price_pe) / 2
        premium = (current_price - avg_implied) / avg_implied
        if premium < -0.20:
            assessment = "SIGNIFICANTLY_UNDERVALUED"
        elif premium < -0.05:
            assessment = "UNDERVALUED"
        elif premium < 0.05:
            assessment = "FAIRLY_VALUED"
        elif premium < 0.20:
            assessment = "OVERVALUED"
        else:
            assessment = "SIGNIFICANTLY_OVERVALUED"
    else:
        assessment = "INSUFFICIENT_DATA"

    return {
        "ticker": ticker,
        "peers": [p["ticker"] for p in valid_peers],
        "subject_metrics": subject,
        "peer_metrics": valid_peers,
        "peer_medians": {
            "ev_ebitda": peer_ev_ebitda,
            "pe_trailing": peer_pe,
            "ev_revenue": peer_ev_revenue,
            "peg_ratio": peer_peg,
        },
        "implied_prices": {
            "from_ev_ebitda": implied_price_ev_ebitda,
            "from_pe": implied_price_pe,
        },
        "relative_valuation_assessment": assessment,
    }


def main():
    parser = argparse.ArgumentParser(description="Comparable company analysis")
    parser.add_argument("ticker", type=str, help="Stock ticker symbol")
    parser.add_argument(
        "--peers", type=str, default=None, help="Comma-separated peer tickers"
    )
    args = parser.parse_args()

    peers = args.peers.split(",") if args.peers else None

    try:
        result = run_comparables(args.ticker.upper(), peers)
        json.dump(result, sys.stdout, indent=2)
        sys.stdout.write("\n")
    except Exception as e:
        json.dump({"error": str(e)}, sys.stderr, indent=2)
        sys.exit(1)


if __name__ == "__main__":
    main()
