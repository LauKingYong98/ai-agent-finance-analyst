"""Pydantic schema for the Valuation Agent output."""

from pydantic import BaseModel, Field


class DCFModel(BaseModel):
    revenue_growth_assumptions: dict[str, float] = Field(
        description="Revenue growth rate assumptions by year, e.g. {'2026': 0.08, '2027': 0.07}"
    )
    terminal_growth_rate: float = Field(description="Terminal growth rate as decimal")
    wacc: float = Field(description="Weighted average cost of capital as decimal")
    operating_margin_assumption: float = Field(description="Assumed steady-state operating margin as decimal")
    implied_share_price: float = Field(description="DCF-implied share price in USD")
    sensitivity_wacc_range: dict[str, float] = Field(
        description="Price sensitivity to WACC, e.g. {'8%': 250, '9%': 220, '10%': 195}"
    )
    sensitivity_growth_range: dict[str, float] = Field(
        description="Price sensitivity to terminal growth, e.g. {'2%': 200, '3%': 220, '4%': 245}"
    )


class ComparableAnalysis(BaseModel):
    peer_companies: list[str] = Field(description="List of peer company tickers used")
    ev_ebitda_peer_median: float = Field(description="Peer median EV/EBITDA multiple")
    ev_ebitda_subject: float = Field(description="Subject company EV/EBITDA multiple")
    pe_peer_median: float = Field(description="Peer median P/E ratio")
    pe_subject: float = Field(description="Subject company P/E ratio")
    peg_ratio: float | None = Field(default=None, description="PEG ratio")
    implied_price_ev_ebitda: float = Field(
        description="Implied price from EV/EBITDA comparable analysis"
    )
    implied_price_pe: float = Field(
        description="Implied price from P/E comparable analysis"
    )
    relative_valuation_assessment: str = Field(
        description="Assessment: SIGNIFICANTLY_UNDERVALUED, UNDERVALUED, FAIRLY_VALUED, OVERVALUED, SIGNIFICANTLY_OVERVALUED"
    )


class ScenarioAnalysis(BaseModel):
    bull_case_price: float = Field(description="Bull case (90th percentile) target price")
    bull_case_assumptions: str = Field(description="Key assumptions for bull case")
    base_case_price: float = Field(description="Base case (median) target price")
    base_case_assumptions: str = Field(description="Key assumptions for base case")
    bear_case_price: float = Field(description="Bear case (10th percentile) target price")
    bear_case_assumptions: str = Field(description="Key assumptions for bear case")
    probability_weighted_price: float = Field(
        description="Probability-weighted target price (20% bull / 60% base / 20% bear)"
    )


class ValuationReport(BaseModel):
    ticker: str = Field(description="Stock ticker symbol")
    current_price: float = Field(description="Current stock price in USD")
    dcf_model: DCFModel
    comparable_analysis: ComparableAnalysis
    scenario_analysis: ScenarioAnalysis
    valuation_summary: str = Field(
        description="3-4 sentence summary of the valuation assessment"
    )
    overall_valuation_signal: str = Field(
        description="Signal: SIGNIFICANTLY_UNDERVALUED, UNDERVALUED, FAIRLY_VALUED, OVERVALUED, SIGNIFICANTLY_OVERVALUED"
    )
