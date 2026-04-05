"""FastAPI backend for the AI Agent Finance Analyst dashboard.

Serves the frontend and provides API endpoints to browse analysis reports.
Reports are generated via Claude Code and stored in workspace/analysis/{ticker}/.
"""

import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="AI Agent Finance Analyst", version="0.1.0")

WORKSPACE_DIR = Path("workspace/analysis")
FRONTEND_DIR = Path("frontend")

# Serve static files
app.mount("/static", StaticFiles(directory=FRONTEND_DIR / "static"), name="static")

# Agent display metadata
AGENT_META = {
    "macro": {
        "name": "Macro Strategist",
        "icon": "globe",
        "color": "#f59e0b",
        "phase": 1,
        "model": "Sonnet 4.6",
    },
    "quant": {
        "name": "Quant Analyst",
        "icon": "chart-line",
        "color": "#3b82f6",
        "phase": 1,
        "model": "Sonnet 4.6",
    },
    "fundamental": {
        "name": "Fundamental Analyst",
        "icon": "building",
        "color": "#10b981",
        "phase": 1,
        "model": "Sonnet 4.6",
    },
    "sentiment": {
        "name": "Sentiment Analyst",
        "icon": "comments",
        "color": "#8b5cf6",
        "phase": 1,
        "model": "Sonnet 4.6",
    },
    "valuation": {
        "name": "Valuation Specialist",
        "icon": "calculator",
        "color": "#06b6d4",
        "phase": 2,
        "model": "Sonnet 4.6",
    },
    "thesis_v1": {
        "name": "Fund Manager (Thesis v1)",
        "icon": "brain",
        "color": "#ec4899",
        "phase": 3,
        "model": "Opus 4.6",
    },
    "red_team": {
        "name": "Red Team",
        "icon": "shield-halved",
        "color": "#ef4444",
        "phase": 4,
        "model": "Opus 4.6",
    },
    "thesis_final": {
        "name": "Fund Manager (Final Thesis)",
        "icon": "crown",
        "color": "#f59e0b",
        "phase": 5,
        "model": "Opus 4.6",
    },
}


@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """Serve the main dashboard page."""
    html_path = FRONTEND_DIR / "index.html"
    if not html_path.exists():
        raise HTTPException(status_code=500, detail="Frontend not found")
    return html_path.read_text()


@app.get("/api/tickers")
async def list_tickers():
    """List all tickers that have analysis reports."""
    if not WORKSPACE_DIR.exists():
        return {"tickers": []}
    tickers = sorted([
        d.name for d in WORKSPACE_DIR.iterdir()
        if d.is_dir() and (d / "thesis_final_report.json").exists()
    ])
    return {"tickers": tickers}


@app.get("/api/analysis/{ticker}")
async def get_analysis(ticker: str):
    """Get all analysis reports for a ticker."""
    ticker = ticker.upper()
    ticker_dir = WORKSPACE_DIR / ticker

    if not ticker_dir.exists():
        raise HTTPException(status_code=404, detail=f"No analysis found for {ticker}")

    reports = {}
    report_files = {
        "macro": "macro_report.json",
        "quant": "quant_report.json",
        "fundamental": "fundamental_report.json",
        "sentiment": "sentiment_report.json",
        "valuation": "valuation_report.json",
        "thesis_v1": "thesis_v1_report.json",
        "red_team": "red_team_report.json",
        "thesis_final": "thesis_final_report.json",
    }

    for key, filename in report_files.items():
        filepath = ticker_dir / filename
        if filepath.exists():
            with open(filepath) as f:
                reports[key] = json.load(f)

    if not reports:
        raise HTTPException(status_code=404, detail=f"No reports found for {ticker}")

    return {
        "ticker": ticker,
        "reports": reports,
        "agent_meta": AGENT_META,
        "completed_phases": _get_completed_phases(reports),
    }


@app.get("/api/analysis/{ticker}/{agent}")
async def get_agent_report(ticker: str, agent: str):
    """Get a specific agent's report for a ticker."""
    ticker = ticker.upper()
    report_files = {
        "macro": "macro_report.json",
        "quant": "quant_report.json",
        "fundamental": "fundamental_report.json",
        "sentiment": "sentiment_report.json",
        "valuation": "valuation_report.json",
        "thesis_v1": "thesis_v1_report.json",
        "red_team": "red_team_report.json",
        "thesis_final": "thesis_final_report.json",
    }

    if agent not in report_files:
        raise HTTPException(status_code=400, detail=f"Unknown agent: {agent}")

    filepath = WORKSPACE_DIR / ticker / report_files[agent]
    if not filepath.exists():
        raise HTTPException(status_code=404, detail=f"No {agent} report for {ticker}")

    with open(filepath) as f:
        return json.load(f)


def _get_completed_phases(reports: dict) -> list[int]:
    """Determine which phases have completed based on available reports."""
    phases = []
    phase_1_agents = {"quant", "fundamental", "sentiment", "macro"}
    if phase_1_agents & reports.keys():
        phases.append(1)
    if "valuation" in reports:
        phases.append(2)
    if "thesis_v1" in reports:
        phases.append(3)
    if "red_team" in reports:
        phases.append(4)
    if "thesis_final" in reports:
        phases.append(5)
    return phases
