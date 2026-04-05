"""Tests for the orchestration pipeline.

These tests validate the pipeline structure and agent definitions
without making actual API calls.
"""

import pytest
from pathlib import Path

from src.agents.definitions import (
    AGENTS,
    PHASE_1_AGENTS,
    PHASE_2_AGENTS,
    PHASE_4_AGENTS,
    QUANT_AGENT,
    FUNDAMENTAL_AGENT,
    SENTIMENT_AGENT,
    VALUATION_AGENT,
    FUND_MANAGER_AGENT,
    RED_TEAM_AGENT,
)
from src.orchestrator import AnalysisPipeline


class TestAgentDefinitions:
    def test_all_agents_registered(self):
        assert len(AGENTS) == 6
        assert set(AGENTS.keys()) == {
            "quant", "fundamental", "sentiment",
            "valuation", "fund_manager", "red_team",
        }

    def test_phase_1_has_three_agents(self):
        assert len(PHASE_1_AGENTS) == 3
        names = {a.name for a in PHASE_1_AGENTS}
        assert names == {"quant", "fundamental", "sentiment"}

    def test_phase_2_has_valuation(self):
        assert len(PHASE_2_AGENTS) == 1
        assert PHASE_2_AGENTS[0].name == "valuation"

    def test_phase_4_has_red_team(self):
        assert len(PHASE_4_AGENTS) == 1
        assert PHASE_4_AGENTS[0].name == "red_team"

    def test_opus_agents_use_opus(self):
        assert "opus" in FUND_MANAGER_AGENT.model
        assert "opus" in RED_TEAM_AGENT.model

    def test_sonnet_agents_use_sonnet(self):
        for agent in [QUANT_AGENT, FUNDAMENTAL_AGENT, SENTIMENT_AGENT, VALUATION_AGENT]:
            assert "sonnet" in agent.model

    def test_all_prompts_exist(self):
        for agent in AGENTS.values():
            prompt = agent.system_prompt
            assert len(prompt) > 100, f"{agent.name} prompt is too short"

    def test_agent_names_match_keys(self):
        for key, agent in AGENTS.items():
            assert key == agent.name


class TestPipelineInit:
    def test_pipeline_creates_output_dir(self, tmp_path, monkeypatch):
        monkeypatch.setattr("src.orchestrator.WORKSPACE_DIR", tmp_path)
        pipeline = AnalysisPipeline("AAPL")
        assert pipeline.ticker == "AAPL"
        assert pipeline.output_dir.exists()

    def test_pipeline_uppercases_ticker(self, tmp_path, monkeypatch):
        monkeypatch.setattr("src.orchestrator.WORKSPACE_DIR", tmp_path)
        pipeline = AnalysisPipeline("aapl")
        assert pipeline.ticker == "AAPL"

    def test_pipeline_verbose_mode(self, tmp_path, monkeypatch):
        monkeypatch.setattr("src.orchestrator.WORKSPACE_DIR", tmp_path)
        pipeline = AnalysisPipeline("AAPL", verbose=True)
        assert pipeline.verbose is True
