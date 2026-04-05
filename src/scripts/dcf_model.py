#!/usr/bin/env python3
"""Discounted Cash Flow (DCF) valuation model.

Usage:
    python -m src.scripts.dcf_model AAPL

Output: JSON to stdout with DCF valuation results.
"""

import argparse
import json
import sys

import yfinance as yf


def get_financials(ticker: str) -> dict:
    """Fetch key financial data for DCF inputs."""
    stock = yf.Ticker(ticker)
    info = stock.info

    revenue = info.get("totalRevenue", 0)
    operating_margin = info.get("operatingMargins", 0.15)
    shares_outstanding = info.get("sharesOutstanding", 1)
    current_price = info.get("currentPrice", info.get("regularMarketPrice", 0))
    free_cash_flow = info.get("freeCashflow", 0)
    total_debt = info.get("totalDebt", 0)
    cash = info.get("totalCash", 0)
    market_cap = info.get("marketCap", 0)
    beta = info.get("beta", 1.0)

    return {
        "revenue": revenue,
        "operating_margin": operating_margin,
        "shares_outstanding": shares_outstanding,
        "current_price": current_price,
        "free_cash_flow": free_cash_flow,
        "total_debt": total_debt,
        "cash": cash,
        "market_cap": market_cap,
        "beta": beta if beta else 1.0,
    }


def estimate_wacc(beta: float, risk_free: float = 0.043, equity_premium: float = 0.055) -> float:
    """Estimate WACC using CAPM for cost of equity (simplified, assumes all-equity)."""
    cost_of_equity = risk_free + beta * equity_premium
    return round(cost_of_equity, 4)


def run_dcf(
    ticker: str,
    growth_rates: list[float] | None = None,
    terminal_growth: float = 0.03,
    projection_years: int = 5,
) -> dict:
    """Run DCF valuation model."""
    financials = get_financials(ticker)

    if growth_rates is None:
        base_growth = 0.08
        growth_rates = [round(base_growth * (0.9**i), 4) for i in range(projection_years)]

    wacc = estimate_wacc(financials["beta"])
    fcf = financials["free_cash_flow"]
    shares = financials["shares_outstanding"]

    if fcf <= 0 or shares <= 0:
        return {
            "ticker": ticker,
            "error": "Insufficient data for DCF (negative FCF or missing shares)",
            "current_price": financials["current_price"],
            "financials": {
                "revenue": financials["revenue"],
                "free_cash_flow": fcf,
                "shares_outstanding": shares,
            },
        }

    # Project future free cash flows
    projected_fcf = []
    current_fcf = fcf
    for rate in growth_rates:
        current_fcf = current_fcf * (1 + rate)
        projected_fcf.append(current_fcf)

    # Terminal value (Gordon Growth Model)
    terminal_value = projected_fcf[-1] * (1 + terminal_growth) / (wacc - terminal_growth)

    # Discount cash flows to present value
    pv_fcfs = []
    for i, cf in enumerate(projected_fcf):
        pv = cf / (1 + wacc) ** (i + 1)
        pv_fcfs.append(pv)

    pv_terminal = terminal_value / (1 + wacc) ** projection_years

    enterprise_value = sum(pv_fcfs) + pv_terminal
    equity_value = enterprise_value - financials["total_debt"] + financials["cash"]
    implied_price = equity_value / shares

    # Sensitivity analysis
    sensitivity_wacc = {}
    for wacc_adj in [-0.02, -0.01, 0, 0.01, 0.02]:
        adj_wacc = wacc + wacc_adj
        if adj_wacc <= terminal_growth:
            continue
        adj_tv = projected_fcf[-1] * (1 + terminal_growth) / (adj_wacc - terminal_growth)
        adj_pv_fcfs = [cf / (1 + adj_wacc) ** (i + 1) for i, cf in enumerate(projected_fcf)]
        adj_pv_tv = adj_tv / (1 + adj_wacc) ** projection_years
        adj_ev = sum(adj_pv_fcfs) + adj_pv_tv
        adj_eq = adj_ev - financials["total_debt"] + financials["cash"]
        sensitivity_wacc[f"{adj_wacc:.1%}"] = round(adj_eq / shares, 2)

    sensitivity_growth = {}
    for tg_adj in [-0.01, 0, 0.01, 0.02]:
        adj_tg = terminal_growth + tg_adj
        if adj_tg >= wacc:
            continue
        adj_tv = projected_fcf[-1] * (1 + adj_tg) / (wacc - adj_tg)
        adj_pv_tv = adj_tv / (1 + wacc) ** projection_years
        adj_ev = sum(pv_fcfs) + adj_pv_tv
        adj_eq = adj_ev - financials["total_debt"] + financials["cash"]
        sensitivity_growth[f"{adj_tg:.1%}"] = round(adj_eq / shares, 2)

    return {
        "ticker": ticker,
        "current_price": financials["current_price"],
        "wacc": round(wacc, 4),
        "terminal_growth_rate": terminal_growth,
        "projection_years": projection_years,
        "growth_rates": {f"year_{i+1}": r for i, r in enumerate(growth_rates)},
        "projected_fcf": [round(f, 0) for f in projected_fcf],
        "pv_fcfs": [round(f, 0) for f in pv_fcfs],
        "terminal_value": round(terminal_value, 0),
        "pv_terminal_value": round(pv_terminal, 0),
        "enterprise_value": round(enterprise_value, 0),
        "equity_value": round(equity_value, 0),
        "implied_share_price": round(implied_price, 2),
        "upside_downside": f"{((implied_price / financials['current_price']) - 1) * 100:.1f}%"
        if financials["current_price"] > 0
        else "N/A",
        "sensitivity_wacc": sensitivity_wacc,
        "sensitivity_terminal_growth": sensitivity_growth,
    }


def main():
    parser = argparse.ArgumentParser(description="DCF valuation model")
    parser.add_argument("ticker", type=str, help="Stock ticker symbol")
    parser.add_argument(
        "--terminal-growth", type=float, default=0.03, help="Terminal growth rate"
    )
    parser.add_argument(
        "--projection-years", type=int, default=5, help="Number of projection years"
    )
    args = parser.parse_args()

    try:
        result = run_dcf(
            args.ticker.upper(),
            terminal_growth=args.terminal_growth,
            projection_years=args.projection_years,
        )
        json.dump(result, sys.stdout, indent=2)
        sys.stdout.write("\n")
    except Exception as e:
        json.dump({"error": str(e)}, sys.stderr, indent=2)
        sys.exit(1)


if __name__ == "__main__":
    main()
