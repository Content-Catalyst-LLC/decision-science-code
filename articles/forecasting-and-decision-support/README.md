# Forecasting and Decision Support

This companion directory supports the article **"Forecasting and Decision Support."**

The workflows operationalize forecasting as a decision-support practice rather than a standalone prediction exercise. They include forecast-error metrics, probabilistic calibration, threshold decisions, value-of-information proxies, forecast-horizon diagnostics, reference-class checks, early-warning signal monitoring, and decision-record scaffolding.

## Core Claim

Forecasts estimate what may happen. Decision support helps determine what should be done given uncertainty, consequences, values, constraints, and available evidence. A forecast is useful only when it improves the quality of a decision.

## Modeling Principles

1. Define the decision before building the forecast.
2. Specify the forecast target, time horizon, and resolution criteria.
3. Use base rates and reference classes before case-specific adjustment.
4. Represent uncertainty with probabilities, intervals, distributions, or scenarios.
5. Evaluate forecast quality using error, calibration, horizon, and decision value.
6. Connect forecast probabilities to explicit decision thresholds.
7. Test sensitivity across assumptions, horizons, models, and scenarios.
8. Estimate whether forecast information improves decisions enough to justify its cost.
9. Monitor drift, early-warning signals, forecast error, and threshold breaches.
10. Preserve forecasts, assumptions, decisions, outcomes, and review triggers in decision records.

## Quick Start

From this article directory:

```bash
python3 python/run_all_forecasting_workflows.py
Rscript r/run_all_forecasting_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
