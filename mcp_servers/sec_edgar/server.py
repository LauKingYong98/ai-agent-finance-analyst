#!/usr/bin/env python3
"""MCP Server for SEC EDGAR API access.

Provides tools for agents to fetch SEC filings, company facts,
and financial data from the SEC EDGAR system.

Requires SEC_EDGAR_EMAIL environment variable (SEC fair access policy).
"""

import json
import os

import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("sec-edgar", description="SEC EDGAR filing and financial data access")

BASE_URL = "https://data.sec.gov"
EFTS_URL = "https://efts.sec.gov/LATEST"
SUBMISSION_URL = f"{BASE_URL}/submissions"
COMPANY_FACTS_URL = f"{BASE_URL}/api/xbrl/companyfacts"


def _get_headers() -> dict:
    """Get request headers with required User-Agent for SEC fair access."""
    email = os.environ.get("SEC_EDGAR_EMAIL", "finance-analyst@example.com")
    return {
        "User-Agent": f"AI-Agent-Finance-Analyst {email}",
        "Accept": "application/json",
    }


def _cik_to_padded(cik: str | int) -> str:
    """Pad CIK to 10 digits as required by SEC API."""
    return str(cik).zfill(10)


@mcp.tool()
def search_company(query: str) -> str:
    """Search for a company by name or ticker to get its CIK number.

    Args:
        query: Company name or ticker symbol (e.g., "Apple" or "AAPL")

    Returns:
        JSON string with matching companies and their CIK numbers
    """
    url = f"{EFTS_URL}/search-index?q={query}&dateRange=custom&startdt=2020-01-01&forms=10-K"
    try:
        with httpx.Client(timeout=15) as client:
            resp = client.get(url, headers=_get_headers())
            resp.raise_for_status()
            data = resp.json()

        hits = data.get("hits", {}).get("hits", [])
        results = []
        seen_ciks = set()
        for hit in hits[:10]:
            source = hit.get("_source", {})
            cik = source.get("entity_id", "")
            if cik in seen_ciks:
                continue
            seen_ciks.add(cik)
            results.append({
                "cik": cik,
                "entity_name": source.get("entity_name", ""),
                "ticker": source.get("tickers", ""),
                "form_type": source.get("form_type", ""),
                "filing_date": source.get("file_date", ""),
            })

        return json.dumps({"query": query, "results": results}, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_company_filings(cik: str, form_type: str = "10-K", count: int = 5) -> str:
    """Get recent filings for a company by CIK number.

    Args:
        cik: Company CIK number (will be zero-padded)
        form_type: SEC form type filter (e.g., "10-K", "10-Q", "8-K")
        count: Number of recent filings to return (max 20)

    Returns:
        JSON string with filing details including accession numbers and dates
    """
    padded_cik = _cik_to_padded(cik)
    url = f"{SUBMISSION_URL}/CIK{padded_cik}.json"

    try:
        with httpx.Client(timeout=15) as client:
            resp = client.get(url, headers=_get_headers())
            resp.raise_for_status()
            data = resp.json()

        company_name = data.get("name", "")
        recent = data.get("filings", {}).get("recent", {})

        forms = recent.get("form", [])
        dates = recent.get("filingDate", [])
        accessions = recent.get("accessionNumber", [])
        primary_docs = recent.get("primaryDocument", [])
        descriptions = recent.get("primaryDocDescription", [])

        filings = []
        for i in range(len(forms)):
            if form_type and forms[i] != form_type:
                continue
            filings.append({
                "form_type": forms[i],
                "filing_date": dates[i] if i < len(dates) else "",
                "accession_number": accessions[i] if i < len(accessions) else "",
                "primary_document": primary_docs[i] if i < len(primary_docs) else "",
                "description": descriptions[i] if i < len(descriptions) else "",
            })
            if len(filings) >= count:
                break

        return json.dumps({
            "cik": cik,
            "company_name": company_name,
            "form_type_filter": form_type,
            "filings": filings,
        }, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_company_facts(cik: str) -> str:
    """Get XBRL company facts (financial data points) from SEC.

    Returns key financial metrics reported in SEC filings. This includes
    revenue, net income, assets, EPS, and many other standardized fields.

    Args:
        cik: Company CIK number (will be zero-padded)

    Returns:
        JSON string with key financial facts (summarized to most recent values)
    """
    padded_cik = _cik_to_padded(cik)
    url = f"{COMPANY_FACTS_URL}/CIK{padded_cik}.json"

    try:
        with httpx.Client(timeout=15) as client:
            resp = client.get(url, headers=_get_headers())
            resp.raise_for_status()
            data = resp.json()

        entity_name = data.get("entityName", "")
        facts = data.get("facts", {})

        # Extract key US-GAAP metrics
        us_gaap = facts.get("us-gaap", {})
        key_metrics = [
            "Revenues", "RevenueFromContractWithCustomerExcludingAssessedTax",
            "NetIncomeLoss", "OperatingIncomeLoss",
            "EarningsPerShareBasic", "EarningsPerShareDiluted",
            "Assets", "Liabilities", "StockholdersEquity",
            "OperatingCashFlow", "NetCashProvidedByOperatingActivities",
            "CommonStockSharesOutstanding",
        ]

        result_metrics = {}
        for metric in key_metrics:
            if metric in us_gaap:
                units = us_gaap[metric].get("units", {})
                # Get the most common unit (usually USD or shares)
                for unit_type, values in units.items():
                    if values:
                        # Get the most recent annual (10-K) filing value
                        annual_values = [
                            v for v in values
                            if v.get("form") == "10-K"
                        ]
                        if annual_values:
                            latest = annual_values[-1]
                            result_metrics[metric] = {
                                "value": latest.get("val"),
                                "unit": unit_type,
                                "period_end": latest.get("end"),
                                "form": latest.get("form"),
                                "filed": latest.get("filed"),
                            }
                    break  # Only take the first unit type

        return json.dumps({
            "cik": cik,
            "entity_name": entity_name,
            "key_metrics": result_metrics,
        }, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


@mcp.tool()
def get_filing_text(cik: str, accession_number: str, document: str) -> str:
    """Fetch the text content of a specific SEC filing document.

    Use get_company_filings first to find the accession_number and document name.

    Args:
        cik: Company CIK number
        accession_number: Filing accession number (e.g., "0000320193-23-000106")
        document: Primary document filename (e.g., "aapl-20230930.htm")

    Returns:
        First 5000 characters of the filing text (to keep response manageable)
    """
    padded_cik = _cik_to_padded(cik)
    accession_clean = accession_number.replace("-", "")
    url = f"{BASE_URL}/Archives/edgar/data/{padded_cik}/{accession_clean}/{document}"

    try:
        with httpx.Client(timeout=30) as client:
            resp = client.get(url, headers=_get_headers())
            resp.raise_for_status()
            text = resp.text

        # Truncate to keep response manageable
        truncated = len(text) > 5000
        return json.dumps({
            "cik": cik,
            "accession_number": accession_number,
            "document": document,
            "content_length": len(text),
            "truncated": truncated,
            "text": text[:5000],
        }, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})


if __name__ == "__main__":
    mcp.run()
