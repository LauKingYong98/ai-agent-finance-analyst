#!/usr/bin/env python3
"""MCP Server wrapping yfinance for structured financial data access.

Provides tools for agents to fetch stock info, financials, price history,
and key metrics via the Model Context Protocol.
"""

import json
from datetime import datetime

import yfinance as yf
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("yahoo-finance", description="Yahoo Finance data access via yfinance")


@mcp.tool()
def get_stock_info(ticker: str) -> str:
    """Get comprehensive stock information including price, market cap, sector, and key ratios.

    Args:
        ticker: Stock ticker symbol (e.g., "AAPL")

    Returns:
        JSON string with stock information
    """
    stock = yf.Ticker(ticker)
    info = stock.info

    result = {
        "ticker": ticker,
        "name": info.get("longName", ""),
        "sector": info.get("sector", ""),
        "industry": info.get("industry", ""),
        "current_price": info.get("currentPrice", info.get("regularMarketPrice")),
        "market_cap": info.get("marketCap"),
        "enterprise_value": info.get("enterpriseValue"),
        "pe_trailing": info.get("trailingPE"),
        "pe_forward": info.get("forwardPE"),
        "peg_ratio": info.get("pegRatio"),
        "price_to_book": info.get("priceToBook"),
        "ev_to_ebitda": info.get("enterpriseToEbitda"),
        "ev_to_revenue": info.get("enterpriseToRevenue"),
        "profit_margins": info.get("profitMargins"),
        "operating_margins": info.get("operatingMargins"),
        "gross_margins": info.get("grossMargins"),
        "revenue_growth": info.get("revenueGrowth"),
        "earnings_growth": info.get("earningsGrowth"),
        "return_on_equity": info.get("returnOnEquity"),
        "return_on_assets": info.get("returnOnAssets"),
        "debt_to_equity": info.get("debtToEquity"),
        "current_ratio": info.get("currentRatio"),
        "free_cash_flow": info.get("freeCashflow"),
        "total_cash": info.get("totalCash"),
        "total_debt": info.get("totalDebt"),
        "total_revenue": info.get("totalRevenue"),
        "ebitda": info.get("ebitda"),
        "shares_outstanding": info.get("sharesOutstanding"),
        "beta": info.get("beta"),
        "52_week_high": info.get("fiftyTwoWeekHigh"),
        "52_week_low": info.get("fiftyTwoWeekLow"),
        "50_day_average": info.get("fiftyDayAverage"),
        "200_day_average": info.get("twoHundredDayAverage"),
        "dividend_yield": info.get("dividendYield"),
        "payout_ratio": info.get("payoutRatio"),
        "analyst_target_mean": info.get("targetMeanPrice"),
        "analyst_target_median": info.get("targetMedianPrice"),
        "analyst_target_low": info.get("targetLowPrice"),
        "analyst_target_high": info.get("targetHighPrice"),
        "recommendation_key": info.get("recommendationKey"),
        "number_of_analyst_opinions": info.get("numberOfAnalystOpinions"),
    }
    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def get_financial_statements(ticker: str, statement_type: str = "income") -> str:
    """Get financial statements (income, balance sheet, or cash flow).

    Args:
        ticker: Stock ticker symbol (e.g., "AAPL")
        statement_type: One of "income", "balance_sheet", or "cash_flow"

    Returns:
        JSON string with financial statement data (annual, last 4 years)
    """
    stock = yf.Ticker(ticker)

    if statement_type == "income":
        df = stock.financials
    elif statement_type == "balance_sheet":
        df = stock.balance_sheet
    elif statement_type == "cash_flow":
        df = stock.cashflow
    else:
        return json.dumps({"error": f"Unknown statement type: {statement_type}"})

    if df is None or df.empty:
        return json.dumps({"error": f"No {statement_type} data found for {ticker}"})

    result = {
        "ticker": ticker,
        "statement_type": statement_type,
        "data": {},
    }

    for col in df.columns:
        period_key = col.strftime("%Y-%m-%d") if isinstance(col, datetime) else str(col)
        result["data"][period_key] = {
            str(idx): float(val) if val == val else None
            for idx, val in df[col].items()
        }

    return json.dumps(result, indent=2, default=str)


@mcp.tool()
def get_price_history(ticker: str, period: str = "1y", interval: str = "1d") -> str:
    """Get historical price data.

    Args:
        ticker: Stock ticker symbol (e.g., "AAPL")
        period: Data period. Valid: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
        interval: Data interval. Valid: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo

    Returns:
        JSON string with price history (last 20 data points to keep response manageable)
    """
    stock = yf.Ticker(ticker)
    hist = stock.history(period=period, interval=interval)

    if hist.empty:
        return json.dumps({"error": f"No price history found for {ticker}"})

    # Return summary stats + last 20 data points
    recent = hist.tail(20)
    data_points = []
    for date, row in recent.iterrows():
        data_points.append({
            "date": date.strftime("%Y-%m-%d"),
            "open": round(float(row["Open"]), 2),
            "high": round(float(row["High"]), 2),
            "low": round(float(row["Low"]), 2),
            "close": round(float(row["Close"]), 2),
            "volume": int(row["Volume"]),
        })

    result = {
        "ticker": ticker,
        "period": period,
        "interval": interval,
        "total_data_points": len(hist),
        "price_range": {
            "high": round(float(hist["High"].max()), 2),
            "low": round(float(hist["Low"].min()), 2),
        },
        "latest_close": round(float(hist["Close"].iloc[-1]), 2),
        "recent_data": data_points,
    }
    return json.dumps(result, indent=2)


@mcp.tool()
def get_key_metrics(ticker: str) -> str:
    """Get key financial metrics and ratios for quick reference.

    Args:
        ticker: Stock ticker symbol (e.g., "AAPL")

    Returns:
        JSON string with key metrics
    """
    stock = yf.Ticker(ticker)
    info = stock.info

    # Calculate additional metrics
    revenue = info.get("totalRevenue", 0)
    net_income = info.get("netIncomeToCommon", 0)
    fcf = info.get("freeCashflow", 0)
    market_cap = info.get("marketCap", 0)
    ev = info.get("enterpriseValue", 0)

    result = {
        "ticker": ticker,
        "valuation": {
            "market_cap": market_cap,
            "enterprise_value": ev,
            "pe_trailing": info.get("trailingPE"),
            "pe_forward": info.get("forwardPE"),
            "peg_ratio": info.get("pegRatio"),
            "ev_ebitda": info.get("enterpriseToEbitda"),
            "ev_revenue": info.get("enterpriseToRevenue"),
            "price_to_book": info.get("priceToBook"),
            "price_to_fcf": round(market_cap / fcf, 2) if fcf and fcf > 0 else None,
        },
        "profitability": {
            "gross_margin": info.get("grossMargins"),
            "operating_margin": info.get("operatingMargins"),
            "net_margin": info.get("profitMargins"),
            "roe": info.get("returnOnEquity"),
            "roa": info.get("returnOnAssets"),
            "roic": round(net_income / (info.get("totalDebt", 0) + market_cap), 4)
            if market_cap > 0
            else None,
        },
        "growth": {
            "revenue_growth": info.get("revenueGrowth"),
            "earnings_growth": info.get("earningsGrowth"),
        },
        "financial_health": {
            "current_ratio": info.get("currentRatio"),
            "debt_to_equity": info.get("debtToEquity"),
            "total_cash": info.get("totalCash"),
            "total_debt": info.get("totalDebt"),
            "free_cash_flow": fcf,
        },
    }
    return json.dumps(result, indent=2, default=str)


if __name__ == "__main__":
    mcp.run()
