# AI Agent Finance Analyst

## Project Overview
Multi-agent investment analysis system using Claude Agent SDK. Six specialized agents collaborate in a fan-out/fan-in pattern with adversarial review to produce investment theses.

## Architecture
- See `docs/ARCHITECTURE.md` for full system design
- 5-phase pipeline: Parallel Analysis -> Valuation -> Synthesis -> Adversarial Review -> Final Thesis
- Fan-out/fan-in orchestration pattern

## Agent Model Assignments
- **Fund Manager**: Opus 4.6 (orchestrator, synthesis, final thesis)
- **Red Team**: Opus 4.6 (adversarial review requires strongest reasoning)
- **Quant / Fundamental / Sentiment / Valuation**: Sonnet 4.6 (data analysis agents)

## Key Conventions
- All agent outputs must validate against Pydantic schemas in `src/agents/schemas/`
- Reports are written to `workspace/analysis/{ticker}/` as JSON
- Python computation scripts in `src/scripts/` are invoked via subprocess by agents
- MCP servers provide structured access to Yahoo Finance and SEC EDGAR data

## Commands
```bash
# Run analysis
python -m src.main analyze AAPL

# Run tests
pytest tests/

# Lint
ruff check src/ tests/
```

## Output Schema Rules
- All JSON output files must conform to their Pydantic schema
- Conviction scores: integer 1-10
- Recommendations: BUY / HOLD / SELL only
- Price targets must include bull/base/bear scenarios
- Dates in ISO 8601 format
