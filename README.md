# AI Agent Finance Analyst

A multi-agent investment analysis system powered by Claude. Seven specialized AI agents collaborate in a fan-out/fan-in pattern with adversarial review, replicating a professional buy-side research team.

> **HOLD AAPL at 5/10 conviction** — that's what this system produced in its first analysis, after the Red Team argued that correlated regulatory risks (DOJ + EU DMA + China tariffs) warranted lowering conviction from 6 to 5.

![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Claude](https://img.shields.io/badge/Claude-Opus%204.6%20%7C%20Sonnet%204.6-purple)
![Tests](https://img.shields.io/badge/Tests-33%20passing-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## How It Works

```
                    ┌─────────────────────────────────┐
                    │         User: "Analyze AAPL"     │
                    └──────────────┬──────────────────┘
                                   │
                    ┌──────────────▼──────────────────┐
                    │     PHASE 1: Parallel Analysis    │
                    │  ┌────────┐ ┌────────┐ ┌──────┐ │
                    │  │ Quant  │ │ Funda- │ │Senti-│ │
                    │  │Analyst │ │mental  │ │ment  │ │
                    │  │Sonnet  │ │Sonnet  │ │Sonnet│ │
                    │  └────┬───┘ └───┬────┘ └──┬───┘ │
                    │  ┌────┴─────────┴─────────┴───┐ │
                    │  │     Macro Strategist        │ │
                    │  │         Sonnet              │ │
                    │  └─────────────────────────────┘ │
                    └──────────────┬──────────────────┘
                                   │
                    ┌──────────────▼──────────────────┐
                    │  PHASE 2: Valuation (Sonnet)     │
                    │  DCF + Comps + Scenario Analysis  │
                    └──────────────┬──────────────────┘
                                   │
                    ┌──────────────▼──────────────────┐
                    │  PHASE 3: Fund Manager (Opus)    │
                    │  Synthesize → Thesis v1           │
                    └──────────────┬──────────────────┘
                                   │
                    ┌──────────────▼──────────────────┐
                    │  PHASE 4: Red Team (Opus)        │
                    │  Challenge assumptions & stress   │
                    │  test valuation                   │
                    └──────────────┬──────────────────┘
                                   │
                    ┌──────────────▼──────────────────┐
                    │  PHASE 5: Fund Manager (Opus)    │
                    │  Integrate Red Team → Final Thesis│
                    └──────────────┬──────────────────┘
                                   │
                    ┌──────────────▼──────────────────┐
                    │   HOLD · Conviction 5/10         │
                    │   Bull $340 · Base $245 · Bear $155│
                    └─────────────────────────────────┘
```

---

## Agent Roster

| Agent | Model | Role | Phase |
|-------|-------|------|-------|
| **Quant Analyst** | Sonnet 4.6 | Technical indicators, risk metrics, factor exposure | 1 (parallel) |
| **Fundamental Analyst** | Sonnet 4.6 | Business quality, moat analysis, financial health | 1 (parallel) |
| **Sentiment Analyst** | Sonnet 4.6 | Material events, analyst consensus, insider activity | 1 (parallel) |
| **Macro Strategist** | Sonnet 4.6 | Market regime, geopolitics, rates, sector rotation | 1 (parallel) |
| **Valuation Specialist** | Sonnet 4.6 | DCF model, comparable analysis, scenario analysis | 2 (sequential) |
| **Fund Manager** | Opus 4.6 | Orchestrator — synthesizes all reports into thesis | 3 & 5 |
| **Red Team** | Opus 4.6 | Adversarial review — challenges assumptions, stress tests | 4 |

---

## Quick Start

### Prerequisites

- Python 3.11+
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) with a Claude Max subscription

### 1. Clone & Install

```bash
git clone https://github.com/LauKingYong98/ai-agent-finance-analyst.git
cd ai-agent-finance-analyst
pip install -e ".[dev]"
```

### 2. Run an Analysis (via Claude Code)

Open the project in Claude Code and ask:

```
analyze AAPL
```

Claude Code will:
1. Run Python data scripts (technical analysis, risk metrics, DCF, comps) on real market data via yfinance
2. Spawn Quant, Fundamental, Sentiment, and Macro agents in parallel
3. Spawn the Valuation agent with Phase 1 context
4. Synthesize Thesis v1 as the Fund Manager
5. Spawn the Red Team to adversarially challenge the thesis
6. Produce the final investment thesis with conviction adjustment

All reports are saved to `workspace/analysis/{TICKER}/`.

### 3. View Results in the Dashboard

```bash
uvicorn src.api:app --reload
```

Open **http://localhost:8000** in your browser. Enter a ticker to see:

- Final thesis with recommendation, conviction meter, and price targets
- Pipeline progress across all 5 phases
- Expandable cards for each agent's report
- Red Team challenges with severity ratings and historical analogies
- Full raw JSON for every report

---

## Web Dashboard

The dashboard provides a dark finance-terminal UI to browse analysis results:

- **Thesis Hero Card** — Recommendation badge, conviction meter (1-10), price targets (bull/base/bear), executive summary
- **Pipeline Visualization** — Phase 1 through 5 completion status
- **Agent Report Cards** — Click any card to expand the full report in a modal
- **Red Team Detail View** — Assumption challenges with severity ratings, valuation stress tests, historical analogies, falsification criteria
- **Catalysts & Risks** — Side-by-side view of key catalysts and key risks

### API Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /` | Dashboard UI |
| `GET /api/tickers` | List all analyzed tickers |
| `GET /api/analysis/{ticker}` | All reports for a ticker |
| `GET /api/analysis/{ticker}/{agent}` | Specific agent report |

---

## Project Structure

```
ai-agent-finance-analyst/
├── frontend/                          # Web dashboard
│   ├── index.html                     # Main page
│   └── static/
│       ├── styles.css                 # Dark theme styles
│       └── app.js                     # Dashboard logic
│
├── src/
│   ├── api.py                         # FastAPI backend
│   ├── main.py                        # CLI entry point
│   ├── orchestrator.py                # Pipeline documentation
│   │
│   ├── agents/
│   │   ├── definitions.py             # Agent definitions (7 agents)
│   │   ├── prompts/                   # System prompts (one per agent)
│   │   │   ├── quant.md
│   │   │   ├── fundamental.md
│   │   │   ├── sentiment.md
│   │   │   ├── macro.md
│   │   │   ├── valuation.md
│   │   │   ├── fund_manager.md
│   │   │   └── red_team.md
│   │   └── schemas/                   # Pydantic output schemas
│   │       ├── quant.py
│   │       ├── fundamental.py
│   │       ├── sentiment.py
│   │       ├── macro.py
│   │       ├── valuation.py
│   │       ├── thesis.py
│   │       └── red_team.py
│   │
│   └── scripts/                       # Python computation scripts
│       ├── technical_analysis.py      # RSI, MACD, Bollinger, MA
│       ├── risk_metrics.py            # Beta, Sharpe, VaR, drawdown
│       ├── dcf_model.py               # DCF valuation engine
│       └── comparables.py             # Comparable company analysis
│
├── mcp_servers/                       # MCP data servers
│   ├── yahoo_finance/server.py        # yfinance wrapper
│   └── sec_edgar/server.py            # SEC EDGAR API
│
├── workspace/                         # Runtime output (gitignored)
│   └── analysis/{TICKER}/             # Per-ticker reports
│       ├── quant_report.json
│       ├── fundamental_report.json
│       ├── sentiment_report.json
│       ├── macro_report.json
│       ├── valuation_report.json
│       ├── thesis_v1_report.json
│       ├── red_team_report.json
│       └── thesis_final_report.json
│
├── tests/                             # Test suite (33 tests)
├── docs/ARCHITECTURE.md               # Full architecture with Mermaid diagrams
├── CLAUDE.md                          # Claude Code project instructions
└── pyproject.toml                     # Dependencies & config
```

---

## Output Schema

The final thesis JSON follows this structure:

```json
{
  "ticker": "AAPL",
  "date": "2026-04-05",
  "recommendation": "HOLD",
  "conviction": 5,
  "target_price": {
    "bull": 340.00,
    "base": 245.00,
    "bear": 155.00
  },
  "current_price": 255.92,
  "time_horizon": "12 months",
  "key_catalysts": ["iPhone 17 super-cycle", "..."],
  "key_risks": ["145% China tariffs", "..."],
  "executive_summary": "Apple remains an exceptional business...",
  "red_team_summary": {
    "strongest_challenge": "Correlated regulatory risks...",
    "thesis_adjustment": "Conviction reduced from 6 to 5...",
    "unresolved_questions": ["..."]
  }
}
```

### Schema Rules

- **Recommendation**: BUY, HOLD, or SELL only
- **Conviction**: Integer 1-10
- **Price targets**: Must include bull, base, and bear scenarios
- **Dates**: ISO 8601 format
- All JSON outputs validated against Pydantic schemas

---

## How the Analysis Pipeline Works

### Phase 1: Parallel Analysis

Four agents run simultaneously:
- **Quant Agent** runs `technical_analysis.py` and `risk_metrics.py` on real yfinance data, then interprets RSI, MACD, Bollinger Bands, beta, Sharpe ratio, VaR, and factor exposure
- **Fundamental Agent** researches business quality, competitive moat (Porter's Five Forces), financial health (margins, FCF, ROIC), and management quality
- **Sentiment Agent** scans for material events, analyst consensus (buy/hold/sell counts, target prices), insider activity, and upcoming catalysts
- **Macro Strategist** assesses market regime, geopolitical risks, Fed policy, inflation, yield curve, and recommends a conviction adjustment based on the macro environment

### Phase 2: Valuation

The **Valuation Agent** receives all Phase 1 reports and:
- Runs `dcf_model.py` with adjusted growth assumptions informed by the Fundamental report
- Runs `comparables.py` against mega-cap peers
- Builds bull/base/bear scenarios using insights from all reports
- Computes a probability-weighted target price (20% bull / 60% base / 20% bear)

### Phase 3: Synthesis

The **Fund Manager** (Opus 4.6) synthesizes all reports into Thesis v1:
- Identifies where agents agree and disagree
- Weighs quantitative evidence over qualitative assertions
- Sets initial recommendation and conviction score

### Phase 4: Adversarial Review

The **Red Team** (Opus 4.6) challenges the thesis:
- 3-5 assumption challenges with severity ratings
- 3-4 valuation stress tests (WACC+200bps, growth halved, etc.)
- 3-5 missing risks the thesis failed to address
- 2-3 historical analogies (e.g., "Microsoft 1999 antitrust")
- Recommends conviction adjustment (0 to -3)

### Phase 5: Final Thesis

The **Fund Manager** considers the Red Team's challenges:
- Accepts or rebuts each challenge point
- Adjusts conviction if warranted
- Produces the final investment thesis

---

## Testing

```bash
# Run all tests
pytest tests/ -v

# 33 tests covering:
# - Pydantic schema validation (8 tests)
# - Computation scripts with synthetic data (12 tests)
# - Agent definitions and pipeline structure (10 tests)
# - API layer logic (3 tests)
```

---

## Tech Stack

| Component | Technology |
|-----------|-----------|
| AI Models | Claude Opus 4.6, Claude Sonnet 4.6 |
| Orchestration | Claude Code (Agent tool) |
| Schemas | Pydantic v2 |
| Market Data | yfinance |
| Financial Data | SEC EDGAR API |
| Computation | NumPy, Pandas |
| Backend | FastAPI, Uvicorn |
| Frontend | Vanilla JS, CSS (dark theme) |
| Data Servers | MCP (Model Context Protocol) |

---

## License

MIT
