# Decision Science in Financial Risk Management

This companion directory supports the article **"Decision Science in Financial Risk Management."**

The workflows operationalize financial risk decision science as a reproducible decision-science problem involving portfolio stress testing, regime analysis, capital resilience, liquidity pressure, tail shocks, model risk, risk appetite, scenario robustness, governance review, systemic exposure, AI model governance, and decision-record scaffolding.

## Core Claim

Financial risk management is not only a technical discipline centered on volatility, value-at-risk, pricing models, hedging, stress testing, and regulatory compliance. It is a decision-science problem: how should institutions choose when the future is only partially knowable, models are imperfect, incentives are unstable, and the institution itself may amplify the risk it is trying to manage?

## Modeling Principles

1. Treat financial risk as part of a decision system, not only a measurement problem.
2. Distinguish measurable risk, uncertainty, ambiguity, deep uncertainty, and model error.
3. Test portfolios across regimes rather than trusting one historical calibration.
4. Evaluate capital, liquidity, funding, collateral, and survivability together.
5. Treat model risk as decision risk.
6. Include governance, incentives, behavioral bias, and independent challenge.
7. Test tail events, liquidity disappearance, correlation breakdown, and management-action realism.
8. Preserve risk appetite, risk capacity, escalation triggers, and decision authority.
9. Treat AI and machine learning as governed components of model-risk architecture.
10. Preserve assumptions, overlays, stress results, dissent, alternatives, and revision triggers in decision records.

## Quick Start

From this article directory:

```bash
python3 python/run_all_financial_risk_workflows.py
Rscript r/run_all_financial_risk_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
