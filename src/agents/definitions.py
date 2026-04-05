"""Agent definitions for the multi-agent finance analysis system.

Each agent is defined with its model, system prompt path, output schema,
and available tools. The orchestrator uses these definitions to spawn agents.
"""

from dataclasses import dataclass, field
from pathlib import Path

PROMPTS_DIR = Path(__file__).parent / "prompts"


@dataclass
class AgentDefinition:
    """Definition of a specialized analysis agent."""

    name: str
    model: str
    prompt_file: str
    description: str
    tools: list[str] = field(default_factory=list)
    mcp_servers: list[str] = field(default_factory=list)

    @property
    def system_prompt(self) -> str:
        """Load the system prompt from the markdown file."""
        prompt_path = PROMPTS_DIR / self.prompt_file
        return prompt_path.read_text()


# Phase 1 agents — run in parallel
QUANT_AGENT = AgentDefinition(
    name="quant",
    model="claude-sonnet-4-6-20250514",
    prompt_file="quant.md",
    description="Quantitative analysis: technical indicators, risk metrics, factor exposure",
    tools=["bash"],
    mcp_servers=["yahoo-finance"],
)

FUNDAMENTAL_AGENT = AgentDefinition(
    name="fundamental",
    model="claude-sonnet-4-6-20250514",
    prompt_file="fundamental.md",
    description="Fundamental analysis: business quality, industry, financial health",
    tools=["bash", "web_search", "web_fetch"],
    mcp_servers=["yahoo-finance", "sec-edgar"],
)

SENTIMENT_AGENT = AgentDefinition(
    name="sentiment",
    model="claude-sonnet-4-6-20250514",
    prompt_file="sentiment.md",
    description="Sentiment analysis: material events, analyst consensus, insider activity",
    tools=["web_search", "web_fetch"],
    mcp_servers=[],
)

MACRO_AGENT = AgentDefinition(
    name="macro",
    model="claude-sonnet-4-6-20250514",
    prompt_file="macro.md",
    description="Macro strategy: market regime, geopolitics, rates, sector rotation",
    tools=["web_search", "web_fetch"],
    mcp_servers=[],
)

# Phase 2 agent — runs after Phase 1 completes
VALUATION_AGENT = AgentDefinition(
    name="valuation",
    model="claude-sonnet-4-6-20250514",
    prompt_file="valuation.md",
    description="Valuation: DCF model, comparable analysis, scenario analysis",
    tools=["bash"],
    mcp_servers=["yahoo-finance"],
)

# Phase 3 + 5 — Fund Manager (orchestrator/synthesizer)
FUND_MANAGER_AGENT = AgentDefinition(
    name="fund_manager",
    model="claude-opus-4-6-20250514",
    prompt_file="fund_manager.md",
    description="Fund Manager: synthesizes all reports into investment thesis",
    tools=[],
    mcp_servers=[],
)

# Phase 4 agent — adversarial review
RED_TEAM_AGENT = AgentDefinition(
    name="red_team",
    model="claude-opus-4-6-20250514",
    prompt_file="red_team.md",
    description="Red Team: adversarial challenge of the investment thesis",
    tools=["web_search"],
    mcp_servers=[],
)


# All agent definitions indexed by name
AGENTS: dict[str, AgentDefinition] = {
    "quant": QUANT_AGENT,
    "fundamental": FUNDAMENTAL_AGENT,
    "sentiment": SENTIMENT_AGENT,
    "macro": MACRO_AGENT,
    "valuation": VALUATION_AGENT,
    "fund_manager": FUND_MANAGER_AGENT,
    "red_team": RED_TEAM_AGENT,
}

# Phase groupings for the orchestrator
PHASE_1_AGENTS = [QUANT_AGENT, FUNDAMENTAL_AGENT, SENTIMENT_AGENT, MACRO_AGENT]
PHASE_2_AGENTS = [VALUATION_AGENT]
PHASE_4_AGENTS = [RED_TEAM_AGENT]
