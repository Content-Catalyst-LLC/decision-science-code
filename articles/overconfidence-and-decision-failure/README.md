# Overconfidence and Decision Failure

This companion directory supports the article **"Overconfidence and Decision Failure."**

The workflows operationalize overconfidence as a decision-system risk involving confidence error, probability calibration, Brier scoring, interval coverage, planning fallacy, optimism bias, overprecision, model overtrust, review triggers, and decision-record scaffolding.

## Core Claim

Overconfidence is not confidence. It is confidence that exceeds evidence, accuracy, uncertainty, track record, or validated model performance. Decision failure becomes more likely when unjustified certainty narrows search, suppresses dissent, hides uncertainty, underestimates downside risk, and weakens contingency planning.

## Modeling Principles

1. Separate confidence from accuracy.
2. Record forecasts before outcomes are known.
3. Score forecast probabilities against outcomes.
4. Evaluate calibration by probability bin, domain, evidence quality, and time horizon.
5. Check whether stated intervals contain actual outcomes.
6. Compare planning estimates with actual cost and duration.
7. Use outside-view reference classes to discipline optimistic inside-view planning.
8. Treat model outputs as uncertain claims, not authoritative facts.
9. Use review triggers for forecast drift, planning error, interval undercoverage, and confidence error.
10. Preserve decision records for confidence, assumptions, evidence, dissent, uncertainty ranges, selected action, and post-decision learning.

## Quick Start

From this article directory:

```bash
python3 python/run_all_overconfidence_workflows.py
Rscript r/run_all_overconfidence_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
