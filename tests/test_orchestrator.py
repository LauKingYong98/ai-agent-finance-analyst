"""Tests for the orchestration pipeline.

These tests validate the pipeline structure, agent definitions,
and the API layer without making actual API calls.
"""

import json
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
    MACRO_AGENT,
)


class TestAgentDefinitions:
    def test_all_agents_registered(self):
        assert len(AGENTS) == 7
        assert set(AGENTS.keys()) == {
            "quant", "fundamental", "sentiment", "macro",
            "valuation", "fund_manager", "red_team",
        }

    def test_phase_1_has_four_agents(self):
        assert len(PHASE_1_AGENTS) == 4
        names = {a.name for a in PHASE_1_AGENTS}
        assert names == {"quant", "fundamental", "sentiment", "macro"}

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
        for agent in [QUANT_AGENT, FUNDAMENTAL_AGENT, SENTIMENT_AGENT, VALUATION_AGENT, MACRO_AGENT]:
            assert "sonnet" in agent.model

    def test_all_prompts_exist(self):
        for agent in AGENTS.values():
            prompt = agent.system_prompt
            assert len(prompt) > 100, f"{agent.name} prompt is too short"

    def test_agent_names_match_keys(self):
        for key, agent in AGENTS.items():
            assert key == agent.name

    def test_macro_agent_has_web_tools(self):
        assert "web_search" in MACRO_AGENT.tools
        assert "web_fetch" in MACRO_AGENT.tools


class TestAPIEndpoints:
    """Test the FastAPI API layer."""

    def test_api_imports(self):
        from src.api import app, AGENT_META
        assert app is not None
        assert "macro" in AGENT_META
        assert "quant" in AGENT_META
        assert len(AGENT_META) == 8  # 7 agents + thesis_final

    def test_agent_meta_has_required_fields(self):
        from src.api import AGENT_META
        for key, meta in AGENT_META.items():
            assert "name" in meta
            assert "icon" in meta
            assert "color" in meta
            assert "phase" in meta
            assert "model" in meta

    def test_completed_phases_logic(self):
        from src.api import _get_completed_phases
        # No reports
        assert _get_completed_phases({}) == []
        # Phase 1 only
        assert _get_completed_phases({"quant": {}}) == [1]
        # Full pipeline
        full = {"quant": {}, "fundamental": {}, "sentiment": {}, "macro": {},
                "valuation": {}, "thesis_v1": {}, "red_team": {}, "thesis_final": {}}
        assert _get_completed_phases(full) == [1, 2, 3, 4, 5]
