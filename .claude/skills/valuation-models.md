---
name: valuation-models
description: DCF and comparable analysis methodology reference
user-invocable: true
---

# Valuation Models — Methodology Reference

## DCF (Discounted Cash Flow)

### Steps
1. **Project Free Cash Flows** for 5 years based on revenue growth and margin assumptions
2. **Calculate Terminal Value** using Gordon Growth Model: TV = FCF_n * (1 + g) / (WACC - g)
3. **Discount to Present**: PV = FCF_t / (1 + WACC)^t
4. **Enterprise Value** = Sum of PV(FCFs) + PV(Terminal Value)
5. **Equity Value** = Enterprise Value - Net Debt
6. **Implied Price** = Equity Value / Shares Outstanding

### WACC Estimation (Simplified CAPM)
- Cost of Equity = Risk-Free Rate + Beta * Equity Risk Premium
- Default assumptions: Risk-Free = 4.3%, ERP = 5.5%

### Terminal Growth Rate Guidelines
- Mature companies: 2-3%
- Growing companies: 3-4%
- Never exceed long-term GDP growth (~4%)

## Comparable Analysis

### Steps
1. **Select Peers**: Same sector/industry, similar size and growth profile
2. **Compute Multiples**: EV/EBITDA, P/E, EV/Revenue, PEG
3. **Find Peer Medians**: Central tendency of peer multiples
4. **Apply to Subject**: Implied EV = Peer Median Multiple * Subject's Metric
5. **Derive Price**: (Implied EV - Net Debt) / Shares Outstanding

### Multiple Interpretation
- **EV/EBITDA**: Most common; sector-neutral. Tech: 15-25x, Industrial: 8-12x
- **P/E**: Earnings-based. Growth: 25-40x, Value: 10-18x
- **PEG**: P/E divided by growth rate. < 1 = undervalued, > 2 = expensive

## Scenario Analysis Weights
- Bull (90th percentile): 20% probability
- Base (median): 60% probability
- Bear (10th percentile): 20% probability
- **Probability-Weighted Price** = 0.2 * Bull + 0.6 * Base + 0.2 * Bear
