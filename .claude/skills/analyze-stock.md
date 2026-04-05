---
name: analyze-stock
description: Run end-to-end stock analysis using the multi-agent pipeline
user-invocable: true
---

# Analyze Stock Skill

Run the full multi-agent investment analysis pipeline for a given stock ticker.

## Usage
When the user invokes `/analyze-stock AAPL`, execute:

```bash
python -m src.main analyze {ticker} --verbose
```

## What It Does
1. **Phase 1** — Dispatches Quant, Fundamental, and Sentiment agents in parallel
2. **Phase 2** — Runs Valuation agent with Phase 1 context
3. **Phase 3** — Fund Manager synthesizes Thesis v1
4. **Phase 4** — Red Team challenges the thesis
5. **Phase 5** — Fund Manager produces final investment thesis

## Output
- All reports saved to `workspace/analysis/{TICKER}/`
- Final thesis displayed in the terminal with recommendation, conviction, target prices
- Individual agent reports available as JSON files

## Prerequisites
- `ANTHROPIC_API_KEY` must be set in `.env` or environment
- Python dependencies installed: `pip install -e ".[dev]"`
