# Probability Calibration and Decision Confidence

This companion directory supports the article **"Probability Calibration and Decision Confidence."**

The workflows operationalize probability calibration as a reproducible decision-science practice. They include Brier scoring, log-loss scoring, reliability-table construction, expected calibration error, confidence-bias diagnostics, base-rate checks, decision-threshold calibration, model-calibration monitoring, and decision-record scaffolding.

## Core Claim

Probability calibration tests whether stated confidence matches observed outcomes. A decision-maker who assigns 70 percent probability to many events should be correct roughly 70 percent of the time across similar judgments. When confidence is miscalibrated, decisions can become overconfident, underprepared, delayed, falsely precise, or poorly governed.

## Modeling Principles

1. Define the forecasted event before estimating probability.
2. Use base rates and reference classes before case-specific adjustment.
3. Express confidence as probability or probability range when decision-relevant.
4. Score probability judgments after outcomes resolve.
5. Distinguish calibration, accuracy, discrimination, resolution, and sharpness.
6. Test calibration across probability bins, domains, and confidence profiles.
7. Connect calibrated probabilities to action thresholds.
8. Audit model scores before treating them as probabilities.
9. Preserve forecasts, thresholds, outcomes, and reasoning in decision records.
10. Treat calibration as a feedback loop for judgment, not as a substitute for responsibility.

## Quick Start

From this article directory:

```bash
python3 python/run_all_calibration_workflows.py
Rscript r/run_all_calibration_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
