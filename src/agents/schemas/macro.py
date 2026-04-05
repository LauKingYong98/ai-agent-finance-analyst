"""Pydantic schema for the Macro Strategist Agent output."""

from pydantic import BaseModel, Field


class MarketRegime(BaseModel):
    regime: str = Field(
        description="Current market regime: RISK_ON, RISK_OFF, TRANSITIONING, CRISIS"
    )
    sp500_trend: str = Field(description="S&P 500 trend: UPTREND, DOWNTREND, SIDEWAYS")
    vix_level: str = Field(description="VIX level characterization: LOW (<15), NORMAL (15-20), ELEVATED (20-30), HIGH (>30)")
    market_breadth: str = Field(description="Market breadth: STRONG, MODERATE, WEAK, VERY_WEAK")
    regime_summary: str = Field(description="2-3 sentence summary of current market regime")


class GeopoliticalRisks(BaseModel):
    major_conflicts: list[str] = Field(
        description="Active major conflicts affecting markets (e.g., 'Middle East conflict disrupting shipping lanes')"
    )
    trade_war_status: str = Field(
        description="US-China trade war status summary including tariff levels"
    )
    sanctions_impact: str = Field(
        description="Material sanctions affecting global markets"
    )
    geopolitical_risk_level: str = Field(
        description="Overall geopolitical risk: LOW, MODERATE, ELEVATED, HIGH, EXTREME"
    )


class MacroeconomicFactors(BaseModel):
    fed_funds_rate: str = Field(description="Current Fed funds rate or range")
    rate_direction: str = Field(description="Rate trajectory: HIKING, PAUSING, CUTTING")
    inflation_trend: str = Field(description="Inflation trend: RISING, ELEVATED_STABLE, DECLINING, LOW_STABLE")
    gdp_growth_outlook: str = Field(description="GDP growth outlook: STRONG, MODERATE, SLOW, RECESSION_RISK, RECESSION")
    unemployment_trend: str = Field(description="Unemployment trend: FALLING, STABLE, RISING")
    yield_curve: str = Field(description="Yield curve status: NORMAL, FLAT, INVERTED, STEEPENING")
    dollar_trend: str = Field(description="USD trend: STRENGTHENING, STABLE, WEAKENING")
    credit_conditions: str = Field(description="Credit conditions: LOOSE, NORMAL, TIGHTENING, TIGHT")


class SectorRotation(BaseModel):
    leading_sectors: list[str] = Field(description="Top 3 leading sectors in current rotation")
    lagging_sectors: list[str] = Field(description="Top 3 lagging sectors")
    rotation_signal: str = Field(
        description="What the rotation pattern suggests: EARLY_CYCLE, MID_CYCLE, LATE_CYCLE, DEFENSIVE"
    )


class MacroReport(BaseModel):
    date: str = Field(description="Analysis date in ISO 8601 format")
    market_regime: MarketRegime
    geopolitical_risks: GeopoliticalRisks
    macroeconomic_factors: MacroeconomicFactors
    sector_rotation: SectorRotation
    macro_headwinds: list[str] = Field(
        description="Top 3-5 macro headwinds for equity markets"
    )
    macro_tailwinds: list[str] = Field(
        description="Top 3-5 macro tailwinds for equity markets"
    )
    risk_appetite_score: int = Field(
        ge=1, le=10,
        description="Market risk appetite score 1 (extreme fear) to 10 (extreme greed)"
    )
    investment_implications: str = Field(
        description="3-4 sentence summary of what the macro environment means for stock picking"
    )
    macro_adjustment_recommendation: str = Field(
        description="How should individual stock conviction be adjusted given macro: BOOST (+1), NEUTRAL (0), REDUCE (-1), STRONGLY_REDUCE (-2)"
    )
