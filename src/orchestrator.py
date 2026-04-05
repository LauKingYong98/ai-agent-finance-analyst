"""5-phase fan-out/fan-in orchestration pipeline.

This pipeline is designed to run natively within Claude Code, using:
- Bash tool to execute Python data scripts (yfinance, computations)
- Agent tool to spawn specialized subagents (Quant, Fundamental, Sentiment, Valuation, Red Team)
- Claude Code itself acts as the Fund Manager (orchestrator + synthesizer)

No Anthropic API key required — runs on the user's Claude Max subscription via Claude Code.

Phases:
    1. Parallel Analysis — Run data scripts + spawn Quant, Fundamental, Sentiment agents
    2. Valuation — Spawn Valuation agent with Phase 1 reports as context
    3. Synthesis — Fund Manager (Claude Code) synthesizes Thesis v1
    4. Adversarial Review — Spawn Red Team agent to challenge the thesis
    5. Final Thesis — Fund Manager produces the final investment thesis

Execution: Invoke via Claude Code with `/analyze-stock AAPL` or ask Claude Code
to "analyze AAPL" — Claude Code will orchestrate the full pipeline using its
Agent tool for subagents and Bash tool for data scripts.
"""
