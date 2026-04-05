"""Tests for Python computation scripts.

These tests validate the computation logic using known inputs.
They don't require network access (use synthetic data).
"""

import numpy as np
import pandas as pd
import pytest

from src.scripts.technical_analysis import (
    compute_rsi,
    compute_macd,
    compute_bollinger_bands,
    compute_moving_averages,
    compute_volume_analysis,
)
from src.scripts.risk_metrics import (
    compute_beta,
    compute_sharpe_ratio,
    compute_max_drawdown,
    compute_var,
    compute_annualized_volatility,
)


class TestTechnicalAnalysis:
    @pytest.fixture
    def uptrend_prices(self):
        """Generate an uptrending price series."""
        np.random.seed(42)
        base = np.linspace(100, 150, 250)
        noise = np.random.normal(0, 2, 250)
        return pd.Series(base + noise)

    @pytest.fixture
    def downtrend_prices(self):
        """Generate a downtrending price series."""
        np.random.seed(42)
        base = np.linspace(150, 100, 250)
        noise = np.random.normal(0, 2, 250)
        return pd.Series(base + noise)

    def test_rsi_range(self, uptrend_prices):
        rsi = compute_rsi(uptrend_prices)
        assert 0 <= rsi <= 100

    def test_rsi_uptrend_high(self, uptrend_prices):
        rsi = compute_rsi(uptrend_prices)
        assert rsi > 50  # Uptrend should produce RSI > 50

    def test_rsi_downtrend_low(self, downtrend_prices):
        rsi = compute_rsi(downtrend_prices)
        assert rsi < 50  # Downtrend should produce RSI < 50

    def test_macd_returns_all_fields(self, uptrend_prices):
        result = compute_macd(uptrend_prices)
        assert "macd_line" in result
        assert "signal_line" in result
        assert "histogram" in result
        assert result["signal"] in ("BULLISH", "BEARISH", "NEUTRAL")

    def test_bollinger_bands_ordering(self, uptrend_prices):
        result = compute_bollinger_bands(uptrend_prices)
        assert result["lower"] < result["middle"] < result["upper"]
        assert result["position"] in (
            "ABOVE_UPPER", "UPPER_HALF", "LOWER_HALF", "BELOW_LOWER"
        )

    def test_moving_averages(self, uptrend_prices):
        result = compute_moving_averages(uptrend_prices)
        assert "sma_50" in result
        assert "sma_200" in result
        assert result["crossover"] in ("GOLDEN_CROSS", "DEATH_CROSS", "NONE")

    def test_volume_analysis(self):
        # Increasing volume
        volume = pd.Series(list(range(100, 200)) * 1)
        padded = pd.Series([50] * 60 + list(range(100, 200)))
        result = compute_volume_analysis(padded)
        assert result["trend"] in ("INCREASING", "DECREASING", "STABLE")
        assert result["avg_volume_30d"] > 0


class TestRiskMetrics:
    @pytest.fixture
    def stock_returns(self):
        np.random.seed(42)
        return pd.Series(np.random.normal(0.001, 0.02, 252))

    @pytest.fixture
    def benchmark_returns(self):
        np.random.seed(43)
        return pd.Series(np.random.normal(0.0005, 0.015, 252))

    def test_beta_positive(self, stock_returns, benchmark_returns):
        # With random data, beta should be finite
        beta = compute_beta(stock_returns, benchmark_returns)
        assert np.isfinite(beta)

    def test_sharpe_ratio_finite(self, stock_returns):
        sharpe = compute_sharpe_ratio(stock_returns)
        assert np.isfinite(sharpe)

    def test_max_drawdown_negative(self):
        # A series that goes up then down
        prices = pd.Series([100, 110, 120, 90, 95, 80, 100])
        dd = compute_max_drawdown(prices)
        assert dd < 0  # Drawdown should be negative
        assert dd >= -1  # Can't lose more than 100%

    def test_max_drawdown_no_drawdown(self):
        # Monotonically increasing series
        prices = pd.Series([100, 110, 120, 130, 140])
        dd = compute_max_drawdown(prices)
        assert dd == 0.0

    def test_var_negative(self, stock_returns):
        var = compute_var(stock_returns, 0.95)
        assert var < 0  # VaR should be negative (loss)

    def test_volatility_positive(self, stock_returns):
        vol = compute_annualized_volatility(stock_returns)
        assert vol > 0
