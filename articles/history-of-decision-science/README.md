# The History of Decision Science

This companion directory supports the article **"The History of Decision Science."**

The workflows model the historical development of decision science as a sequence of expanding decision paradigms: expected monetary value, expected utility, subjective probability, Bayesian updating, bounded rationality, satisficing, behavioral noise, minimax regret, robustness, and decision records.

## Core Claim

The history of decision science is not the replacement of one theory by another. It is the accumulation of increasingly realistic decision lenses for reasoning under uncertainty, incomplete information, cognitive constraint, strategic interaction, systems complexity, and institutional accountability.

## Modeling Principles

1. Treat historical paradigms as complementary decision lenses.
2. Use expected value when probabilities and payoffs are credible.
3. Use expected utility when risk attitude and subjective value matter.
4. Use subjective probability when repeated frequencies are unavailable.
5. Use Bayesian updating when evidence changes beliefs.
6. Use satisficing to model bounded rationality and limited search.
7. Use regret and robustness when forecasts are fragile or futures are contested.
8. Document assumptions and decision records so historical model choices remain reviewable.
9. Treat computational models as supports for judgment, not substitutes for responsibility.

## Quick Start

From this article directory:

```bash
python3 python/run_all_history_workflows.py
Rscript r/run_all_history_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
