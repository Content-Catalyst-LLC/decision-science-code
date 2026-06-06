# Heuristics and Cognitive Biases

This companion directory supports the article **"Heuristics and Cognitive Biases."**

The workflows operationalize heuristics and cognitive biases as measurable process risks in decision science. They include synthetic judgment-case generation, anchoring distortion, availability salience weighting, representativeness and base-rate neglect, confirmation-bias asymmetry, overconfidence, calibration error, confidence-gap diagnostics, debiasing review queues, domain-level bias summaries, and decision-record scaffolding.

## Core Claim

Heuristics simplify judgment under uncertainty. They can be adaptive when they fit the decision environment, but they can also produce predictable cognitive biases. Decision science does not try to eliminate intuition. It designs processes that make judgment more explicit, calibrated, testable, and accountable.

## Modeling Principles

1. Treat heuristics as simplification strategies, not automatic errors.
2. Distinguish adaptive shortcuts from systematic bias.
3. Use base rates and reference classes before case-specific adjustment.
4. Collect independent estimates before group discussion.
5. Preserve alternatives, assumptions, dissent, and uncertainty.
6. Measure confidence gaps and calibration error.
7. Use premortems, red teams, and disconfirming evidence search.
8. Flag high-distortion cases for review.
9. Separate decision-process quality from outcome luck.
10. Preserve decision records for learning and accountability.

## Quick Start

From this article directory:

```bash
python3 python/run_all_bias_workflows.py
Rscript r/run_all_bias_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
