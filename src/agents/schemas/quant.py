"""Pydantic schema for the Quant Agent output."""

from pydantic import BaseModel, Field


class TechnicalIndicators(BaseModel):
    rsi_14: float = Field(description="14-day Relative Strength Index")
    macd_signal: str = Field(description="MACD signal: BULLISH, BEARISH, or NEUTRAL")
    macd_histogram: float = Field(description="MACD histogram value")
    bollinger_position: str = Field(
        description="Price position relative to Bollinger Bands: ABOVE_UPPER, UPPER_HALF, LOWER_HALF, BELOW_LOWER"
    )
    sma_50: float = Field(description="50-day simple moving average")
    sma_200: float = Field(description="200-day simple moving average")
    sma_crossover: str = Field(
        description="SMA crossover signal: GOLDEN_CROSS, DEATH_CROSS, or NONE"
    )
    avg_volume_30d: float = Field(description="30-day average daily volume")
    volume_trend: str = Field(description="Volume trend: INCREASING, DECREASING, or STABLE")


class RiskMetrics(BaseModel):
    beta: float = Field(description="Beta vs S&P 500 benchmark")
    sharpe_ratio: float = Field(description="Annualized Sharpe ratio (1yr)")
    max_drawdown: float = Field(description="Maximum drawdown over trailing 1yr, as decimal")
    var_95: float = Field(description="95% Value at Risk (daily), as decimal")
    annualized_volatility: float = Field(description="Annualized volatility, as decimal")


class FactorExposure(BaseModel):
    momentum: str = Field(description="Momentum factor: STRONG_POS, WEAK_POS, NEUTRAL, WEAK_NEG, STRONG_NEG")
    value: str = Field(description="Value factor: DEEP_VALUE, VALUE, FAIR, GROWTH, EXPENSIVE")
    size: str = Field(description="Size factor: MEGA_CAP, LARGE_CAP, MID_CAP, SMALL_CAP, MICRO_CAP")
    quality: str = Field(description="Quality factor: HIGH, ABOVE_AVG, AVERAGE, BELOW_AVG, LOW")


class QuantReport(BaseModel):
    ticker: str = Field(description="Stock ticker symbol")
    current_price: float = Field(description="Current stock price in USD")
    technical_indicators: TechnicalIndicators
    risk_metrics: RiskMetrics
    factor_exposure: FactorExposure
    technical_summary: str = Field(
        description="2-3 sentence summary of the technical picture"
    )
    risk_summary: str = Field(
        description="2-3 sentence summary of the risk profile"
    )
    overall_quant_signal: str = Field(
        description="Overall quant signal: BULLISH, SLIGHTLY_BULLISH, NEUTRAL, SLIGHTLY_BEARISH, BEARISH"
    )
