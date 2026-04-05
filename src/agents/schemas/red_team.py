"""Pydantic schema for the Red Team Agent output."""

from pydantic import BaseModel, Field


class AssumptionChallenge(BaseModel):
    assumption: str = Field(description="The assumption being challenged")
    challenge: str = Field(description="Why this assumption may be wrong")
    evidence: str = Field(description="Supporting evidence or historical precedent")
    severity: str = Field(description="Severity if wrong: CRITICAL, HIGH, MEDIUM, LOW")


class ValuationStressTest(BaseModel):
    scenario: str = Field(description="Stress test scenario description")
    impact_on_valuation: str = Field(
        description="How this scenario changes the valuation, e.g. '-25% to implied price'"
    )
    probability: str = Field(description="Estimated probability: HIGH, MEDIUM, LOW")


class HistoricalAnalogy(BaseModel):
    company_or_situation: str = Field(description="The historical company or situation")
    parallel: str = Field(description="How it parallels the current thesis")
    outcome: str = Field(description="What happened in the historical case")
    lesson: str = Field(description="Key lesson for the current thesis")


class RedTeamChallenge(BaseModel):
    ticker: str = Field(description="Stock ticker symbol")
    thesis_recommendation_reviewed: str = Field(
        description="The recommendation from the thesis being reviewed: BUY, HOLD, or SELL"
    )
    thesis_conviction_reviewed: int = Field(
        description="The conviction score from the thesis being reviewed"
    )
    assumption_challenges: list[AssumptionChallenge] = Field(
        description="3-5 challenges to key assumptions in the thesis"
    )
    valuation_stress_tests: list[ValuationStressTest] = Field(
        description="3-4 valuation stress test scenarios"
    )
    missing_risks: list[str] = Field(
        description="3-5 risks not adequately addressed in the thesis"
    )
    historical_analogies: list[HistoricalAnalogy] = Field(
        description="2-3 historical analogies that serve as cautionary tales"
    )
    strongest_challenge: str = Field(
        description="The single most compelling reason the thesis could be wrong"
    )
    conviction_adjustment: int = Field(
        ge=-3, le=0, description="Recommended conviction adjustment (-3 to 0)"
    )
    conviction_adjustment_rationale: str = Field(
        description="Explanation of why conviction should be adjusted by this amount"
    )
    what_would_make_thesis_wrong: str = Field(
        description="The clearest falsification criteria for this thesis"
    )
    red_team_summary: str = Field(
        description="3-4 sentence summary of the Red Team's overall assessment"
    )
