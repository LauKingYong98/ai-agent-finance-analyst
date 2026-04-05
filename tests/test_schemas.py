"""Tests for Pydantic output schemas."""

import pytest
from pydantic import ValidationError

from src.agents.schemas.quant import QuantReport, TechnicalIndicators, RiskMetrics, FactorExposure
from src.agents.schemas.fundamental import FundamentalReport, BusinessQuality, IndustryAnalysis, FinancialHealth
from src.agents.schemas.sentiment import SentimentReport, MaterialEvent, AnalystConsensus, InsiderActivity, UpcomingCatalyst
from src.agents.schemas.valuation import ValuationReport, DCFModel, ComparableAnalysis, ScenarioAnalysis
from src.agents.schemas.thesis import InvestmentThesis, TargetPrice, RedTeamSummary, AgentReportPaths
from src.agents.schemas.red_team import RedTeamChallenge, AssumptionChallenge, ValuationStressTest, HistoricalAnalogy


class TestQuantSchema:
    def test_valid_quant_report(self):
        report = QuantReport(
            ticker="AAPL",
            current_price=195.50,
            technical_indicators=TechnicalIndicators(
                rsi_14=55.3,
                macd_signal="BULLISH",
                macd_histogram=0.45,
                bollinger_position="UPPER_HALF",
                sma_50=190.0,
                sma_200=185.0,
                sma_crossover="NONE",
                avg_volume_30d=50000000,
                volume_trend="STABLE",
            ),
            risk_metrics=RiskMetrics(
                beta=1.2,
                sharpe_ratio=1.5,
                max_drawdown=-0.15,
                var_95=-0.025,
                annualized_volatility=0.22,
            ),
            factor_exposure=FactorExposure(
                momentum="STRONG_POS",
                value="GROWTH",
                size="MEGA_CAP",
                quality="HIGH",
            ),
            technical_summary="RSI neutral, MACD bullish with positive histogram.",
            risk_summary="Beta of 1.2 indicates slightly above-market risk.",
            overall_quant_signal="SLIGHTLY_BULLISH",
        )
        assert report.ticker == "AAPL"
        assert report.current_price == 195.50
        assert report.technical_indicators.rsi_14 == 55.3

    def test_quant_report_json_roundtrip(self):
        report = QuantReport(
            ticker="MSFT",
            current_price=420.0,
            technical_indicators=TechnicalIndicators(
                rsi_14=65.0, macd_signal="NEUTRAL", macd_histogram=-0.1,
                bollinger_position="UPPER_HALF", sma_50=415.0, sma_200=400.0,
                sma_crossover="NONE", avg_volume_30d=25000000, volume_trend="STABLE",
            ),
            risk_metrics=RiskMetrics(
                beta=0.95, sharpe_ratio=1.8, max_drawdown=-0.12,
                var_95=-0.018, annualized_volatility=0.19,
            ),
            factor_exposure=FactorExposure(
                momentum="WEAK_POS", value="GROWTH", size="MEGA_CAP", quality="HIGH",
            ),
            technical_summary="Test summary",
            risk_summary="Test risk",
            overall_quant_signal="NEUTRAL",
        )
        json_str = report.model_dump_json()
        restored = QuantReport.model_validate_json(json_str)
        assert restored.ticker == "MSFT"


class TestFundamentalSchema:
    def test_valid_fundamental_report(self):
        report = FundamentalReport(
            ticker="AAPL",
            company_name="Apple Inc.",
            sector="Technology",
            industry="Consumer Electronics",
            business_quality=BusinessQuality(
                revenue_model="Hardware + Services; recurring services revenue growing",
                moat_type="BRAND",
                moat_strength="WIDE",
                management_rating="EXCELLENT",
                capital_allocation="Strong buyback program, growing dividend",
                esg_considerations="Supply chain labor practices, carbon neutrality goals",
            ),
            industry_analysis=IndustryAnalysis(
                porters_threat_of_entry="LOW",
                porters_supplier_power="MEDIUM",
                porters_buyer_power="LOW",
                porters_substitutes="MEDIUM",
                porters_rivalry="HIGH",
                tam_billions=500.0,
                industry_growth_rate="5-7% CAGR",
                regulatory_environment="Increasing antitrust scrutiny globally",
                disruption_risk="MEDIUM",
            ),
            financial_health=FinancialHealth(
                revenue_ttm=383000.0,
                revenue_growth_yoy=0.08,
                gross_margin=0.45,
                operating_margin=0.30,
                net_margin=0.25,
                free_cash_flow_ttm=110000.0,
                debt_to_equity=1.5,
                current_ratio=1.1,
                roic=0.35,
                margin_trend="STABLE",
            ),
            competitive_advantages=["Brand loyalty", "Ecosystem lock-in", "Services growth"],
            key_risks=["China concentration", "Smartphone saturation", "Regulatory risk"],
            fundamental_summary="Apple is a high-quality business with a wide moat.",
            overall_fundamental_rating="BUY",
        )
        assert report.company_name == "Apple Inc."
        assert report.business_quality.moat_strength == "WIDE"


class TestSentimentSchema:
    def test_valid_sentiment_report(self):
        report = SentimentReport(
            ticker="AAPL",
            material_events=[
                MaterialEvent(
                    date="2026-01-30",
                    event_type="EARNINGS",
                    headline="Apple beats Q1 estimates",
                    impact="POSITIVE",
                    details="Revenue beat by 3%, EPS beat by 5%",
                ),
            ],
            analyst_consensus=AnalystConsensus(
                buy_count=30,
                hold_count=8,
                sell_count=2,
                consensus_rating="BUY",
                average_target_price=220.0,
                target_price_range="$180 - $260",
                recent_rating_changes=["Goldman upgraded to Buy (2026-02-01)"],
            ),
            insider_activity=InsiderActivity(
                net_insider_transactions_90d="NET_SELLING",
                notable_transactions=["CEO sold $10M in shares (2026-01-15)"],
                institutional_ownership_pct=0.72,
                institutional_trend="STABLE",
            ),
            upcoming_catalysts=[
                UpcomingCatalyst(
                    expected_date="2026-04-30",
                    catalyst_type="EARNINGS",
                    description="Q2 2026 earnings report",
                    potential_impact="HIGH",
                ),
            ],
            sentiment_summary="Overall bullish sentiment with strong analyst support.",
            overall_sentiment="BULLISH",
        )
        assert report.overall_sentiment == "BULLISH"
        assert len(report.material_events) == 1


class TestValuationSchema:
    def test_valid_valuation_report(self):
        report = ValuationReport(
            ticker="AAPL",
            current_price=195.50,
            dcf_model=DCFModel(
                revenue_growth_assumptions={"2026": 0.08, "2027": 0.07, "2028": 0.06},
                terminal_growth_rate=0.03,
                wacc=0.095,
                operating_margin_assumption=0.30,
                implied_share_price=215.00,
                sensitivity_wacc_range={"8.5%": 240, "9.5%": 215, "10.5%": 195},
                sensitivity_growth_range={"2%": 200, "3%": 215, "4%": 235},
            ),
            comparable_analysis=ComparableAnalysis(
                peer_companies=["MSFT", "GOOGL", "META"],
                ev_ebitda_peer_median=20.5,
                ev_ebitda_subject=22.0,
                pe_peer_median=28.0,
                pe_subject=30.0,
                peg_ratio=2.1,
                implied_price_ev_ebitda=210.00,
                implied_price_pe=205.00,
                relative_valuation_assessment="FAIRLY_VALUED",
            ),
            scenario_analysis=ScenarioAnalysis(
                bull_case_price=245.00,
                bull_case_assumptions="AI-driven ASP increases, Services at 20% growth",
                base_case_price=218.00,
                base_case_assumptions="Steady 7-8% revenue growth, stable margins",
                bear_case_price=175.00,
                bear_case_assumptions="China headwinds, margin compression",
                probability_weighted_price=214.60,
            ),
            valuation_summary="DCF and comps suggest modest upside from current levels.",
            overall_valuation_signal="UNDERVALUED",
        )
        assert report.overall_valuation_signal == "UNDERVALUED"


class TestThesisSchema:
    def test_valid_thesis(self):
        thesis = InvestmentThesis(
            ticker="AAPL",
            date="2026-04-05",
            recommendation="BUY",
            conviction=7,
            target_price=TargetPrice(bull=245.0, base=218.0, bear=175.0),
            current_price=195.50,
            time_horizon="12 months",
            key_catalysts=["AI integration", "Services growth"],
            key_risks=["China risk", "Saturation"],
            executive_summary="Apple represents a compelling buy opportunity.",
            red_team_summary=RedTeamSummary(
                strongest_challenge="Services growth assumes no antitrust intervention",
                thesis_adjustment="Conviction reduced from 8 to 7",
                unresolved_questions=["EU Digital Markets Act impact?"],
            ),
            agent_reports=AgentReportPaths(
                quant="workspace/analysis/AAPL/quant_report.json",
                fundamental="workspace/analysis/AAPL/fundamental_report.json",
                sentiment="workspace/analysis/AAPL/sentiment_report.json",
                valuation="workspace/analysis/AAPL/valuation_report.json",
                red_team="workspace/analysis/AAPL/red_team_challenge.json",
            ),
        )
        assert thesis.recommendation == "BUY"
        assert thesis.conviction == 7

    def test_conviction_bounds(self):
        with pytest.raises(ValidationError):
            InvestmentThesis(
                ticker="AAPL", date="2026-04-05", recommendation="BUY",
                conviction=11,  # Out of bounds
                target_price=TargetPrice(bull=245, base=218, bear=175),
                current_price=195.50, time_horizon="12 months",
                key_catalysts=[], key_risks=[],
                executive_summary="Test",
                red_team_summary=RedTeamSummary(
                    strongest_challenge="", thesis_adjustment="",
                    unresolved_questions=[],
                ),
                agent_reports=AgentReportPaths(
                    quant="q", fundamental="f", sentiment="s",
                    valuation="v", red_team="r",
                ),
            )


class TestRedTeamSchema:
    def test_valid_red_team_challenge(self):
        challenge = RedTeamChallenge(
            ticker="AAPL",
            thesis_recommendation_reviewed="BUY",
            thesis_conviction_reviewed=8,
            assumption_challenges=[
                AssumptionChallenge(
                    assumption="Services will grow at 15%+ for 5 years",
                    challenge="Antitrust regulation could force App Store fee reductions",
                    evidence="EU DMA already enacted; US DOJ lawsuit ongoing",
                    severity="HIGH",
                ),
            ],
            valuation_stress_tests=[
                ValuationStressTest(
                    scenario="WACC +200bps",
                    impact_on_valuation="-18% to implied price",
                    probability="MEDIUM",
                ),
            ],
            missing_risks=["Key person risk if Tim Cook departs"],
            historical_analogies=[
                HistoricalAnalogy(
                    company_or_situation="Nokia 2007",
                    parallel="Dominant phone maker with strong brand",
                    outcome="Lost 90% of market share in 5 years",
                    lesson="Moats can erode faster than expected when paradigm shifts",
                ),
            ],
            strongest_challenge="Antitrust risk to Services margins",
            conviction_adjustment=-1,
            conviction_adjustment_rationale="Regulatory risk is underweighted in thesis",
            what_would_make_thesis_wrong="EU/US forces 50%+ App Store fee reduction",
            red_team_summary="The thesis is fundamentally sound but underweights regulatory risk.",
        )
        assert challenge.conviction_adjustment == -1
        assert len(challenge.assumption_challenges) == 1
