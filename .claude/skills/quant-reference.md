---
name: quant-reference
description: Quick reference for quantitative indicator formulas and interpretation
user-invocable: true
---

# Quant Reference — Indicator Formulas

## RSI (Relative Strength Index)
- **Formula**: RSI = 100 - (100 / (1 + RS)), where RS = Avg Gain / Avg Loss over N periods
- **Default period**: 14 days
- **Overbought**: RSI > 70 | **Oversold**: RSI < 30 | **Neutral**: 30-70

## MACD (Moving Average Convergence Divergence)
- **MACD Line**: 12-day EMA - 26-day EMA
- **Signal Line**: 9-day EMA of MACD Line
- **Histogram**: MACD Line - Signal Line
- **Bullish**: Histogram positive and increasing | **Bearish**: Histogram negative and decreasing

## Bollinger Bands
- **Middle**: 20-day SMA
- **Upper**: Middle + 2 * 20-day StdDev
- **Lower**: Middle - 2 * 20-day StdDev
- Price above upper = potential overbought; below lower = potential oversold

## Moving Average Crossovers
- **Golden Cross**: 50-day SMA crosses ABOVE 200-day SMA (bullish)
- **Death Cross**: 50-day SMA crosses BELOW 200-day SMA (bearish)

## Risk Metrics
- **Beta**: Cov(stock, benchmark) / Var(benchmark). Beta > 1 = more volatile than market
- **Sharpe Ratio**: (Return - RiskFree) / StdDev. > 1.0 = good, > 2.0 = excellent
- **Max Drawdown**: Worst peak-to-trough decline. < -20% = significant risk
- **VaR (95%)**: Maximum expected daily loss at 95% confidence
- **Annualized Volatility**: Daily StdDev * sqrt(252)
