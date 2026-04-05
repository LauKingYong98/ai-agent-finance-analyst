"""Pydantic schema for the Fundamental Agent output."""

from pydantic import BaseModel, Field


class BusinessQuality(BaseModel):
    revenue_model: str = Field(description="Description of revenue model and unit economics")
    moat_type: str = Field(
        description="Competitive moat: NETWORK_EFFECT, BRAND, SWITCHING_COST, COST_ADVANTAGE, INTANGIBLE, NONE"
    )
    moat_strength: str = Field(description="Moat strength: WIDE, NARROW, NONE")
    management_rating: str = Field(
        description="Management quality: EXCELLENT, GOOD, ADEQUATE, POOR"
    )
    capital_allocation: str = Field(
        description="Capital allocation track record summary"
    )
    esg_considerations: str = Field(description="Material ESG factors")


class IndustryAnalysis(BaseModel):
    porters_threat_of_entry: str = Field(description="Threat of new entrants: LOW, MEDIUM, HIGH")
    porters_supplier_power: str = Field(description="Supplier bargaining power: LOW, MEDIUM, HIGH")
    porters_buyer_power: str = Field(description="Buyer bargaining power: LOW, MEDIUM, HIGH")
    porters_substitutes: str = Field(description="Threat of substitutes: LOW, MEDIUM, HIGH")
    porters_rivalry: str = Field(description="Competitive rivalry: LOW, MEDIUM, HIGH")
    tam_billions: float | None = Field(default=None, description="Total addressable market in USD billions")
    industry_growth_rate: str = Field(description="Industry growth rate characterization")
    regulatory_environment: str = Field(description="Regulatory environment summary")
    disruption_risk: str = Field(description="Technology disruption risk: LOW, MEDIUM, HIGH")


class FinancialHealth(BaseModel):
    revenue_ttm: float = Field(description="Trailing twelve months revenue in USD millions")
    revenue_growth_yoy: float = Field(description="Year-over-year revenue growth as decimal")
    gross_margin: float = Field(description="Gross margin as decimal")
    operating_margin: float = Field(description="Operating margin as decimal")
    net_margin: float = Field(description="Net margin as decimal")
    free_cash_flow_ttm: float = Field(description="TTM free cash flow in USD millions")
    debt_to_equity: float = Field(description="Debt-to-equity ratio")
    current_ratio: float = Field(description="Current ratio")
    roic: float = Field(description="Return on invested capital as decimal")
    margin_trend: str = Field(description="Margin trend: EXPANDING, STABLE, CONTRACTING")


class FundamentalReport(BaseModel):
    ticker: str = Field(description="Stock ticker symbol")
    company_name: str = Field(description="Full company name")
    sector: str = Field(description="Market sector")
    industry: str = Field(description="Specific industry")
    business_quality: BusinessQuality
    industry_analysis: IndustryAnalysis
    financial_health: FinancialHealth
    competitive_advantages: list[str] = Field(
        description="Top 3-5 competitive advantages"
    )
    key_risks: list[str] = Field(description="Top 3-5 fundamental risks")
    fundamental_summary: str = Field(
        description="3-4 sentence summary of fundamental quality"
    )
    overall_fundamental_rating: str = Field(
        description="Overall rating: STRONG_BUY, BUY, HOLD, SELL, STRONG_SELL"
    )
