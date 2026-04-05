#!/usr/bin/env python3
"""Risk metrics computations: Beta, Sharpe Ratio, VaR, Max Drawdown, Volatility.

Usage:
    python -m src.scripts.risk_metrics AAPL [--benchmark ^GSPC --period 1y]

Output: JSON to stdout with risk metric values.
"""

import argparse
import json
import sys

import numpy as np
import pandas as pd
import yfinance as yf


def compute_beta(stock_returns: pd.Series, benchmark_returns: pd.Series) -> float:
    """Compute beta vs benchmark using covariance method."""
    aligned = pd.concat([stock_returns, benchmark_returns], axis=1).dropna()
    if len(aligned) < 30:
        return float("nan")
    cov = np.cov(aligned.iloc[:, 0], aligned.iloc[:, 1])
    beta = cov[0, 1] / cov[1, 1]
    return round(float(beta), 3)


def compute_sharpe_ratio(
    returns: pd.Series, risk_free_rate: float = 0.045, trading_days: int = 252
) -> float:
    """Compute annualized Sharpe ratio."""
    excess_returns = returns - risk_free_rate / trading_days
    if excess_returns.std() == 0:
        return 0.0
    sharpe = np.sqrt(trading_days) * excess_returns.mean() / excess_returns.std()
    return round(float(sharpe), 3)


def compute_max_drawdown(prices: pd.Series) -> float:
    """Compute maximum drawdown over the period."""
    cumulative_max = prices.cummax()
    drawdown = (prices - cumulative_max) / cumulative_max
    return round(float(drawdown.min()), 4)


def compute_var(returns: pd.Series, confidence: float = 0.95) -> float:
    """Compute historical Value at Risk at given confidence level."""
    var = np.percentile(returns.dropna(), (1 - confidence) * 100)
    return round(float(var), 4)


def compute_annualized_volatility(
    returns: pd.Series, trading_days: int = 252
) -> float:
    """Compute annualized volatility."""
    vol = returns.std() * np.sqrt(trading_days)
    return round(float(vol), 4)


def run_risk_metrics(
    ticker: str, benchmark: str = "^GSPC", period: str = "1y"
) -> dict:
    """Run full risk metrics analysis."""
    stock = yf.Ticker(ticker)
    bench = yf.Ticker(benchmark)

    stock_hist = stock.history(period=period)
    bench_hist = bench.history(period=period)

    if stock_hist.empty:
        raise ValueError(f"No price data found for {ticker}")
    if bench_hist.empty:
        raise ValueError(f"No price data found for benchmark {benchmark}")

    stock_close = stock_hist["Close"]
    bench_close = bench_hist["Close"]

    stock_returns = stock_close.pct_change().dropna()
    bench_returns = bench_close.pct_change().dropna()

    beta = compute_beta(stock_returns, bench_returns)
    sharpe = compute_sharpe_ratio(stock_returns)
    max_dd = compute_max_drawdown(stock_close)
    var_95 = compute_var(stock_returns, 0.95)
    volatility = compute_annualized_volatility(stock_returns)

    return {
        "ticker": ticker,
        "benchmark": benchmark,
        "period": period,
        "beta": beta,
        "sharpe_ratio": sharpe,
        "max_drawdown": max_dd,
        "var_95": var_95,
        "annualized_volatility": volatility,
        "trading_days_analyzed": len(stock_returns),
    }


def main():
    parser = argparse.ArgumentParser(description="Risk metrics for a stock ticker")
    parser.add_argument("ticker", type=str, help="Stock ticker symbol")
    parser.add_argument("--benchmark", type=str, default="^GSPC", help="Benchmark ticker")
    parser.add_argument("--period", type=str, default="1y", help="Data period")
    args = parser.parse_args()

    try:
        result = run_risk_metrics(args.ticker.upper(), args.benchmark, args.period)
        json.dump(result, sys.stdout, indent=2)
        sys.stdout.write("\n")
    except Exception as e:
        json.dump({"error": str(e)}, sys.stderr, indent=2)
        sys.exit(1)


if __name__ == "__main__":
    main()
