"""Pydantic schema for the Fund Manager thesis output."""

from pydantic import BaseModel, Field


class TargetPrice(BaseModel):
    bull: float = Field(description="Bull case target price in USD")
    base: float = Field(description="Base case target price in USD")
    bear: float = Field(description="Bear case target price in USD")


class RedTeamSummary(BaseModel):
    strongest_challenge: str = Field(
        description="The most compelling challenge from the Red Team"
    )
    thesis_adjustment: str = Field(
        description="How the thesis was adjusted in response to the Red Team challenge"
    )
    unresolved_questions: list[str] = Field(
        description="Questions raised by the Red Team that remain unresolved"
    )


class AgentReportPaths(BaseModel):
    quant: str = Field(description="Path to quant report JSON")
    fundamental: str = Field(description="Path to fundamental report JSON")
    sentiment: str = Field(description="Path to sentiment report JSON")
    valuation: str = Field(description="Path to valuation report JSON")
    red_team: str = Field(description="Path to red team challenge JSON")


class InvestmentThesis(BaseModel):
    ticker: str = Field(description="Stock ticker symbol")
    date: str = Field(description="Analysis date in ISO 8601 format")
    recommendation: str = Field(description="Investment recommendation: BUY, HOLD, or SELL")
    conviction: int = Field(ge=1, le=10, description="Conviction score from 1 (lowest) to 10 (highest)")
    target_price: TargetPrice
    current_price: float = Field(description="Current stock price in USD")
    time_horizon: str = Field(description="Investment time horizon, e.g. '12 months'")
    key_catalysts: list[str] = Field(
        description="Top 3-5 catalysts that could drive the stock price toward the target"
    )
    key_risks: list[str] = Field(
        description="Top 3-5 risks that could prevent the thesis from playing out"
    )
    executive_summary: str = Field(
        description="4-6 sentence executive summary of the investment thesis"
    )
    red_team_summary: RedTeamSummary
    agent_reports: AgentReportPaths
