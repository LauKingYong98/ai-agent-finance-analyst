"""Pydantic schema for the Sentiment Agent output."""

from pydantic import BaseModel, Field


class MaterialEvent(BaseModel):
    date: str = Field(description="Event date in ISO 8601 format")
    event_type: str = Field(
        description="Type: EARNINGS, GUIDANCE, M_AND_A, PRODUCT_LAUNCH, LEGAL, REGULATORY, MANAGEMENT_CHANGE, OTHER"
    )
    headline: str = Field(description="Event headline")
    impact: str = Field(description="Impact assessment: VERY_POSITIVE, POSITIVE, NEUTRAL, NEGATIVE, VERY_NEGATIVE")
    details: str = Field(description="1-2 sentence explanation of the event and its significance")


class AnalystConsensus(BaseModel):
    buy_count: int = Field(description="Number of Buy/Outperform ratings")
    hold_count: int = Field(description="Number of Hold/Neutral ratings")
    sell_count: int = Field(description="Number of Sell/Underperform ratings")
    consensus_rating: str = Field(description="Consensus: STRONG_BUY, BUY, HOLD, SELL, STRONG_SELL")
    average_target_price: float | None = Field(
        default=None, description="Average analyst target price in USD"
    )
    target_price_range: str = Field(description="Low-High target price range, e.g. '$150 - $220'")
    recent_rating_changes: list[str] = Field(
        description="Notable recent rating changes, e.g. 'Morgan Stanley upgraded to Overweight (2026-03-15)'"
    )


class InsiderActivity(BaseModel):
    net_insider_transactions_90d: str = Field(
        description="Net insider activity over 90 days: NET_BUYING, NET_SELLING, MIXED, MINIMAL"
    )
    notable_transactions: list[str] = Field(
        description="Notable insider transactions in last 90 days"
    )
    institutional_ownership_pct: float = Field(
        description="Institutional ownership percentage as decimal"
    )
    institutional_trend: str = Field(
        description="Institutional ownership trend: INCREASING, STABLE, DECREASING"
    )


class UpcomingCatalyst(BaseModel):
    expected_date: str = Field(description="Expected date in ISO 8601 format or 'TBD'")
    catalyst_type: str = Field(
        description="Type: EARNINGS, PRODUCT_LAUNCH, REGULATORY_DECISION, CONFERENCE, DIVIDEND, BUYBACK, OTHER"
    )
    description: str = Field(description="Brief description of the upcoming catalyst")
    potential_impact: str = Field(description="Expected impact: HIGH, MEDIUM, LOW")


class SentimentReport(BaseModel):
    ticker: str = Field(description="Stock ticker symbol")
    material_events: list[MaterialEvent] = Field(
        description="Recent material events (last 90 days), ordered by significance"
    )
    analyst_consensus: AnalystConsensus
    insider_activity: InsiderActivity
    upcoming_catalysts: list[UpcomingCatalyst] = Field(
        description="Upcoming catalysts in next 6 months"
    )
    sentiment_summary: str = Field(
        description="3-4 sentence summary of overall market sentiment"
    )
    overall_sentiment: str = Field(
        description="Overall sentiment: VERY_BULLISH, BULLISH, NEUTRAL, BEARISH, VERY_BEARISH"
    )
