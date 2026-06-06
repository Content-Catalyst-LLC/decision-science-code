# Judgment Under Uncertainty

This companion directory supports the article **"Judgment Under Uncertainty."**

The workflows operationalize judgment under uncertainty as a reproducible decision-science problem involving belief formation, prior probabilities, likelihoods, Bayesian-style updating, anchoring distortion, evidence-quality diagnostics, confidence gaps, forecast calibration, Brier scoring, review queues, and decision-record scaffolding.

## Core Claim

Judgment under uncertainty is not merely intuition in the absence of certainty. It is the disciplined formation, revision, and documentation of belief when evidence is incomplete, probabilities are ambiguous, confidence is imperfect, and action may still be required.

## Modeling Principles

1. Define the judgment target before interpreting evidence.
2. Separate prior belief, evidence, posterior belief, forecast probability, and confidence.
3. Use base rates and reference classes before case-specific adjustment.
4. Compare competing hypotheses rather than fitting one preferred story.
5. Evaluate evidence quality before updating confidence.
6. Track anchoring, overconfidence, calibration error, and forecast performance.
7. Use Brier scores and calibration tables for repeated probabilistic judgments.
8. Treat models, dashboards, and AI outputs as supports for judgment, not substitutes for responsibility.
9. Link probability judgments to action thresholds, monitoring triggers, and review conditions.
10. Preserve decision records before outcomes are known to prevent hindsight reconstruction.

## Quick Start

From this article directory:

```bash
python3 python/run_all_judgment_workflows.py
Rscript r/run_all_judgment_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
