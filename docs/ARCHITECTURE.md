# AI Agent Finance Analyst — System Architecture

## Overview

A multi-agent investment analysis system powered by Claude. Six specialized agents collaborate in a fan-out/fan-in pattern with an adversarial review loop, replicating a professional buy-side research team.

**Tech Stack**: Python 3.11+ | Claude Agent SDK | MCP Servers | Pydantic

**Cost**: ~$1.30 per ticker analysis

---

## Agent Roster

| Agent | Model | Role | Input | Output |
|-------|-------|------|-------|--------|
| **Fund Manager** | Opus 4.6 | Orchestrator + synthesizer | All reports | Investment Thesis |
| **Quant** | Sonnet 4.6 | Technical & statistical analysis | Ticker | `quant_report.json` |
| **Fundamental** | Sonnet 4.6 | Business quality + industry analysis | Ticker | `fundamental_report.json` |
| **Sentiment** | Sonnet 4.6 | Material events & market sentiment | Ticker | `sentiment_report.json` |
| **Valuation** | Sonnet 4.6 | Intrinsic value estimation | Ticker + Phase 1 reports | `valuation_report.json` |
| **Red Team** | Opus 4.6 | Adversarial thesis challenge | Thesis v1 + all reports | `red_team_challenge.json` |

---

## System Flowchart

```mermaid
flowchart TB
    subgraph INPUT["INPUT"]
        User["User Input<br/>Ticker Symbol (e.g. AAPL)"]
    end

    subgraph ORCHESTRATOR["FUND MANAGER (Opus 4.6) — Orchestrator"]
        FM_dispatch["Dispatch<br/>Phase 1 Agents"]
        FM_wait1["Collect<br/>Phase 1 Reports"]
        FM_dispatch2["Dispatch<br/>Valuation Agent"]
        FM_wait2["Collect<br/>Valuation Report"]
        FM_synthesize["Synthesize<br/>Thesis v1"]
        FM_dispatch3["Dispatch<br/>Red Team"]
        FM_wait3["Collect<br/>Red Team Challenge"]
        FM_final["Produce<br/>Final Thesis"]
    end

    subgraph PHASE1["PHASE 1 — Parallel Analysis"]
        direction LR
        Quant["Quant Agent<br/>(Sonnet 4.6)<br/>───────────<br/>Technical indicators<br/>Risk metrics<br/>Factor exposure"]
        Fundamental["Fundamental Agent<br/>(Sonnet 4.6)<br/>───────────<br/>Business model & moat<br/>Management quality<br/>Industry dynamics"]
        Sentiment["Sentiment Agent<br/>(Sonnet 4.6)<br/>───────────<br/>Material news events<br/>Analyst consensus<br/>Insider activity"]
    end

    subgraph PHASE2["PHASE 2 — Valuation (Sequential)"]
        Valuation["Valuation Agent<br/>(Sonnet 4.6)<br/>───────────<br/>DCF model<br/>Comparable analysis<br/>Scenario analysis"]
    end

    subgraph PHASE4["PHASE 4 — Adversarial Review"]
        RedTeam["Red Team Agent<br/>(Opus 4.6)<br/>───────────<br/>Challenge assumptions<br/>Stress test valuation<br/>Historical analogies<br/>Identify blind spots"]
    end

    subgraph OUTPUT["OUTPUT"]
        Thesis["Final Investment Thesis<br/>───────────<br/>Recommendation: BUY/HOLD/SELL<br/>Conviction: 1-10<br/>Target Price Range<br/>Key Catalysts & Risks<br/>Red Team Rebuttal"]
    end

    User --> FM_dispatch
    FM_dispatch --> Quant & Fundamental & Sentiment
    Quant & Fundamental & Sentiment --> FM_wait1
    FM_wait1 --> FM_dispatch2
    FM_dispatch2 --> Valuation
    Valuation --> FM_wait2
    FM_wait2 --> FM_synthesize
    FM_synthesize --> FM_dispatch3
    FM_dispatch3 --> RedTeam
    RedTeam --> FM_wait3
    FM_wait3 --> FM_final
    FM_final --> Thesis

    style INPUT fill:#1a1a2e,stroke:#e94560,color:#fff
    style ORCHESTRATOR fill:#16213e,stroke:#0f3460,color:#fff
    style PHASE1 fill:#0f3460,stroke:#533483,color:#fff
    style PHASE2 fill:#0f3460,stroke:#533483,color:#fff
    style PHASE4 fill:#2d132c,stroke:#e94560,color:#fff
    style OUTPUT fill:#1a1a2e,stroke:#00b4d8,color:#fff
```

---

## Execution Timeline

```mermaid
gantt
    title Analysis Pipeline — Execution Phases
    dateFormat X
    axisFormat %s sec

    section Phase 1 (Parallel)
    Quant Agent           :a1, 0, 30
    Fundamental Agent     :a2, 0, 40
    Sentiment Agent       :a3, 0, 25

    section Phase 2 (Sequential)
    Valuation Agent       :a4, after a2, 35

    section Phase 3 (Synthesis)
    Fund Manager — Thesis v1 :a5, after a4, 20

    section Phase 4 (Adversarial)
    Red Team Agent        :a6, after a5, 40

    section Phase 5 (Final)
    Fund Manager — Final  :a7, after a6, 15
```

---

## Data Flow Diagram

```mermaid
flowchart LR
    subgraph DATA_SOURCES["External Data Sources"]
        YF["Yahoo Finance<br/>MCP Server"]
        SEC["SEC EDGAR<br/>MCP Server"]
        WEB["WebSearch /<br/>WebFetch"]
    end

    subgraph SCRIPTS["Python Computation Scripts"]
        TA["technical_analysis.py<br/>RSI, MACD, Bollinger"]
        DCF["dcf_model.py<br/>DCF Valuation"]
        COMP["comparables.py<br/>Peer Analysis"]
        RISK["risk_metrics.py<br/>VaR, Sharpe, Beta"]
    end

    subgraph AGENTS["Agent Layer"]
        Q["Quant"]
        F["Fundamental"]
        S["Sentiment"]
        V["Valuation"]
    end

    subgraph WORKSPACE["workspace/analysis/{ticker}/"]
        QR["quant_report.json"]
        FR["fundamental_report.json"]
        SR["sentiment_report.json"]
        VR["valuation_report.json"]
        T1["thesis_v1.json"]
        RC["red_team_challenge.json"]
        TF["thesis_final.json"]
    end

    YF --> Q & F & V
    SEC --> F
    WEB --> F & S

    Q --> TA & RISK
    V --> DCF & COMP

    TA & RISK --> QR
    Q --> QR
    F --> FR
    S --> SR
    DCF & COMP --> VR
    V --> VR

    QR & FR & SR & VR --> T1
    T1 --> RC
    T1 & RC --> TF

    style DATA_SOURCES fill:#1b263b,stroke:#415a77,color:#fff
    style SCRIPTS fill:#2b2d42,stroke:#8d99ae,color:#fff
    style AGENTS fill:#14213d,stroke:#fca311,color:#fff
    style WORKSPACE fill:#003049,stroke:#d62828,color:#fff
```

---

## Agent Detail — Responsibilities & Tools

### Quant Agent
```mermaid
mindmap
  root((Quant Agent))
    Technical Indicators
      RSI — Relative Strength Index
      MACD — Moving Average Convergence Divergence
      Bollinger Bands
      Moving Averages (50/200 day)
      Volume Analysis
    Risk Metrics
      Beta vs benchmark
      Sharpe Ratio
      Maximum Drawdown
      Value at Risk (VaR)
      Volatility (annualized)
    Factor Exposure
      Momentum
      Value
      Size
      Quality
    Tools
      MCP: Yahoo Finance
      Bash: technical_analysis.py
      Bash: risk_metrics.py
```

### Fundamental Agent
```mermaid
mindmap
  root((Fundamental Agent))
    Business Quality
      Revenue model & unit economics
      Competitive moat type
      Management track record
      Capital allocation history
      ESG considerations
    Industry Analysis
      Porter's Five Forces
      TAM / SAM / SOM
      Industry growth rate
      Regulatory environment
      Technology disruption risk
    Financial Health
      Balance sheet strength
      Free cash flow generation
      Margin trends
      Return on invested capital
    Tools
      MCP: Yahoo Finance
      MCP: SEC EDGAR
      WebSearch
      WebFetch
```

### Sentiment Agent
```mermaid
mindmap
  root((Sentiment Agent))
    Material Events
      Earnings surprises
      Guidance changes
      M&A activity
      Product launches
      Legal/regulatory actions
    Market Sentiment
      Analyst rating changes
      Price target revisions
      Analyst consensus trend
    Insider Activity
      Insider buying/selling
      Institutional holdings changes
    Upcoming Catalysts
      Earnings dates
      Product announcements
      Regulatory decisions
    Tools
      WebSearch
      WebFetch
```

### Valuation Agent
```mermaid
mindmap
  root((Valuation Agent))
    DCF Model
      Revenue projections (3 scenarios)
      Margin assumptions
      WACC calculation
      Terminal growth rate
      Implied share price
    Comparable Analysis
      Peer selection
      EV/EBITDA multiples
      P/E multiples
      PEG ratio
      Relative valuation
    Scenario Analysis
      Bull case (90th percentile)
      Base case (median)
      Bear case (10th percentile)
      Probability-weighted target
    Tools
      MCP: Yahoo Finance
      Bash: dcf_model.py
      Bash: comparables.py
```

### Red Team Agent
```mermaid
mindmap
  root((Red Team Agent))
    Assumption Attacks
      Challenge growth assumptions
      Challenge margin sustainability
      Challenge moat durability
      Challenge management narrative
    Valuation Stress Test
      What if WACC +200bps?
      What if growth halves?
      What if margins compress?
      What if multiple de-rates?
    Missing Risks
      Risks not mentioned in thesis
      Black swan scenarios
      Competitive threats underweighted
      Regulatory risks overlooked
    Historical Analogies
      Similar companies that failed
      Similar theses that were wrong
      Sector-level cautionary tales
    Final Verdict
      Conviction adjustment recommendation
      Key questions that need answers
      "What would make this thesis wrong?"
```

---

## Claude Code Ecosystem Mapping

```mermaid
flowchart TB
    subgraph CLAUDE_MD["CLAUDE.md<br/>核心規範手冊"]
        CM1["Project architecture"]
        CM2["Agent conventions"]
        CM3["Output schema rules"]
        CM4["Model assignment policy"]
        CM5["Testing commands"]
    end

    subgraph SKILLS["Skills<br/>技能懶人包"]
        SK1["analyze-stock<br/>End-to-end workflow"]
        SK2["quant-reference<br/>Indicator formulas"]
        SK3["valuation-models<br/>DCF methodology"]
    end

    subgraph SUBAGENTS["Subagents<br/>分身小助手"]
        SA1["Quant Agent"]
        SA2["Fundamental Agent"]
        SA3["Sentiment Agent"]
        SA4["Valuation Agent"]
        SA5["Red Team Agent"]
    end

    subgraph HOOKS["Hooks<br/>自動化觸發器"]
        HK1["PostToolUse:Write<br/>Schema validation"]
        HK2["PostToolUse:Agent<br/>Cost tracking"]
        HK3["Stop<br/>Auto-summary"]
    end

    subgraph MCP["MCP Servers<br/>外部工具橋樑"]
        MC1["Yahoo Finance<br/>(yfinance wrapper)"]
        MC2["SEC EDGAR<br/>(EDGAR API)"]
        MC3["WebSearch<br/>(built-in)"]
        MC4["WebFetch<br/>(built-in)"]
    end

    CLAUDE_MD --> |"Read on every session"| SUBAGENTS
    SKILLS --> |"Loaded on demand"| SUBAGENTS
    MCP --> |"Data access"| SUBAGENTS
    HOOKS --> |"Quality gates"| SUBAGENTS

    style CLAUDE_MD fill:#e74c3c,stroke:#c0392b,color:#fff
    style SKILLS fill:#f39c12,stroke:#d68910,color:#fff
    style SUBAGENTS fill:#e74c3c,stroke:#c0392b,color:#fff
    style HOOKS fill:#2ecc71,stroke:#27ae60,color:#fff
    style MCP fill:#9b59b6,stroke:#8e44ad,color:#fff
```

---

## Project Structure

```
ai-agent-finance-analyst/
├── CLAUDE.md                           # Core rules for Claude Code sessions
├── pyproject.toml                      # Python project config & dependencies
├── .env.example                        # API key template
│
├── docs/
│   └── ARCHITECTURE.md                 # This file
│
├── src/
│   ├── main.py                         # CLI entry: python -m src.main analyze AAPL
│   ├── orchestrator.py                 # 5-phase fan-out/fan-in pipeline
│   │
│   ├── agents/
│   │   ├── definitions.py              # AgentDefinition objects (5 agents)
│   │   ├── prompts/
│   │   │   ├── quant.md                # Quant system prompt
│   │   │   ├── fundamental.md          # Fundamental system prompt
│   │   │   ├── sentiment.md            # Sentiment system prompt
│   │   │   ├── valuation.md            # Valuation system prompt
│   │   │   ├── fund_manager.md         # Fund Manager system prompt
│   │   │   └── red_team.md             # Red Team system prompt
│   │   └── schemas/
│   │       ├── quant.py                # Pydantic: quant output
│   │       ├── fundamental.py          # Pydantic: fundamental output
│   │       ├── sentiment.py            # Pydantic: sentiment output
│   │       ├── valuation.py            # Pydantic: valuation output
│   │       ├── thesis.py               # Pydantic: thesis output
│   │       └── red_team.py             # Pydantic: red team output
│   │
│   └── scripts/
│       ├── technical_analysis.py       # RSI, MACD, Bollinger, MA
│       ├── dcf_model.py                # DCF valuation engine
│       ├── comparables.py              # Comparable company analysis
│       └── risk_metrics.py             # VaR, Sharpe, Beta, drawdown
│
├── mcp_servers/
│   ├── yahoo_finance/
│   │   └── server.py                   # MCP server: yfinance wrapper
│   └── sec_edgar/
│       └── server.py                   # MCP server: SEC EDGAR API
│
├── .claude/
│   ├── settings.json                   # MCP config + hooks
│   └── skills/
│       ├── analyze-stock.md            # Skill: full analysis workflow
│       ├── quant-reference.md          # Skill: indicator formulas
│       └── valuation-models.md         # Skill: DCF methodology
│
├── workspace/                          # Runtime output (gitignored)
│   └── analysis/{ticker}/              # Per-ticker analysis reports
│
└── tests/
    ├── test_orchestrator.py
    ├── test_schemas.py
    └── test_scripts.py
```

---

## Output Schema — Final Thesis

```json
{
  "ticker": "AAPL",
  "date": "2026-04-05",
  "recommendation": "BUY",
  "conviction": 7,
  "target_price": {
    "bull": 245.00,
    "base": 218.00,
    "bear": 175.00
  },
  "current_price": 195.50,
  "time_horizon": "12 months",
  "key_catalysts": [
    "AI integration across product line driving ASP increases",
    "Services revenue growing 15%+ YoY with expanding margins"
  ],
  "key_risks": [
    "China regulatory and supply chain concentration",
    "Smartphone market saturation in developed markets"
  ],
  "red_team_summary": {
    "strongest_challenge": "Services growth assumes no antitrust intervention...",
    "thesis_adjustment": "Conviction reduced from 8 to 7 due to...",
    "unresolved_questions": [
      "What happens to margins if EU Digital Markets Act forces App Store changes?"
    ]
  },
  "agent_reports": {
    "quant": "workspace/analysis/AAPL/quant_report.json",
    "fundamental": "workspace/analysis/AAPL/fundamental_report.json",
    "sentiment": "workspace/analysis/AAPL/sentiment_report.json",
    "valuation": "workspace/analysis/AAPL/valuation_report.json",
    "red_team": "workspace/analysis/AAPL/red_team_challenge.json"
  }
}
```

---

## Quick Start (After Implementation)

```bash
# 1. Setup
git clone <repo> && cd ai-agent-finance-analyst
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env   # Add your ANTHROPIC_API_KEY

# 2. Run analysis
python -m src.main analyze AAPL

# 3. View results
cat workspace/analysis/AAPL/thesis_final.json
```
