#!/usr/bin/env python3
"""Technical analysis computations: RSI, MACD, Bollinger Bands, Moving Averages.

Usage:
    python -m src.scripts.technical_analysis AAPL [--period 1y]

Output: JSON to stdout with technical indicator values.
"""

import argparse
import json
import sys

import numpy as np
import pandas as pd
import yfinance as yf


def compute_rsi(prices: pd.Series, window: int = 14) -> float:
    """Compute the Relative Strength Index."""
    delta = prices.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=window, min_periods=window).mean()
    avg_loss = loss.rolling(window=window, min_periods=window).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return round(float(rsi.iloc[-1]), 2)


def compute_macd(
    prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9
) -> dict:
    """Compute MACD line, signal line, and histogram."""
    ema_fast = prices.ewm(span=fast, adjust=False).mean()
    ema_slow = prices.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line

    current_hist = float(histogram.iloc[-1])
    prev_hist = float(histogram.iloc[-2])

    if current_hist > 0 and current_hist > prev_hist:
        signal_str = "BULLISH"
    elif current_hist < 0 and current_hist < prev_hist:
        signal_str = "BEARISH"
    else:
        signal_str = "NEUTRAL"

    return {
        "macd_line": round(float(macd_line.iloc[-1]), 4),
        "signal_line": round(float(signal_line.iloc[-1]), 4),
        "histogram": round(current_hist, 4),
        "signal": signal_str,
    }


def compute_bollinger_bands(
    prices: pd.Series, window: int = 20, num_std: float = 2.0
) -> dict:
    """Compute Bollinger Bands and price position."""
    sma = prices.rolling(window=window).mean()
    std = prices.rolling(window=window).std()
    upper = sma + num_std * std
    lower = sma - num_std * std

    current_price = float(prices.iloc[-1])
    upper_val = float(upper.iloc[-1])
    lower_val = float(lower.iloc[-1])
    mid_val = float(sma.iloc[-1])

    if current_price > upper_val:
        position = "ABOVE_UPPER"
    elif current_price > mid_val:
        position = "UPPER_HALF"
    elif current_price > lower_val:
        position = "LOWER_HALF"
    else:
        position = "BELOW_LOWER"

    return {
        "upper": round(upper_val, 2),
        "middle": round(mid_val, 2),
        "lower": round(lower_val, 2),
        "position": position,
    }


def compute_moving_averages(prices: pd.Series) -> dict:
    """Compute 50-day and 200-day SMAs and crossover signal."""
    sma_50 = prices.rolling(window=50).mean()
    sma_200 = prices.rolling(window=200).mean()

    current_50 = float(sma_50.iloc[-1])
    current_200 = float(sma_200.iloc[-1])
    prev_50 = float(sma_50.iloc[-2])
    prev_200 = float(sma_200.iloc[-2])

    if prev_50 <= prev_200 and current_50 > current_200:
        crossover = "GOLDEN_CROSS"
    elif prev_50 >= prev_200 and current_50 < current_200:
        crossover = "DEATH_CROSS"
    else:
        crossover = "NONE"

    return {
        "sma_50": round(current_50, 2),
        "sma_200": round(current_200, 2),
        "crossover": crossover,
    }


def compute_volume_analysis(volume: pd.Series) -> dict:
    """Analyze volume trends."""
    avg_30d = float(volume.tail(30).mean())
    avg_90d = float(volume.tail(90).mean())

    ratio = avg_30d / avg_90d if avg_90d > 0 else 1.0
    if ratio > 1.1:
        trend = "INCREASING"
    elif ratio < 0.9:
        trend = "DECREASING"
    else:
        trend = "STABLE"

    return {
        "avg_volume_30d": round(avg_30d, 0),
        "avg_volume_90d": round(avg_90d, 0),
        "trend": trend,
    }


def run_technical_analysis(ticker: str, period: str = "1y") -> dict:
    """Run full technical analysis for a given ticker."""
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period)

    if hist.empty:
        raise ValueError(f"No price data found for {ticker}")

    close = hist["Close"]
    volume = hist["Volume"]

    rsi = compute_rsi(close)
    macd = compute_macd(close)
    bollinger = compute_bollinger_bands(close)
    ma = compute_moving_averages(close)
    vol = compute_volume_analysis(volume)

    return {
        "ticker": ticker,
        "current_price": round(float(close.iloc[-1]), 2),
        "rsi_14": rsi,
        "macd": macd,
        "bollinger_bands": bollinger,
        "moving_averages": ma,
        "volume": vol,
        "data_points": len(close),
        "period": period,
    }


def main():
    parser = argparse.ArgumentParser(description="Technical analysis for a stock ticker")
    parser.add_argument("ticker", type=str, help="Stock ticker symbol")
    parser.add_argument("--period", type=str, default="1y", help="Data period (default: 1y)")
    args = parser.parse_args()

    try:
        result = run_technical_analysis(args.ticker.upper(), args.period)
        json.dump(result, sys.stdout, indent=2)
        sys.stdout.write("\n")
    except Exception as e:
        json.dump({"error": str(e)}, sys.stderr, indent=2)
        sys.exit(1)


if __name__ == "__main__":
    main()
