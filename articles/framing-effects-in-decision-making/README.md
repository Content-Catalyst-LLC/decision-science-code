# Framing Effects in Decision-Making

This companion directory supports the article **"Framing Effects in Decision-Making."**

The workflows operationalize framing effects as auditable decision-process risks. They include gain-loss framing simulations, reference-point sensitivity, prospect-style valuation, attribute-frame diagnostics, risk-communication format comparison, frame-reversal detection, review queues, and decision-record scaffolding.

## Core Claim

Framing effects show that decisions are shaped not only by facts, probabilities, outcomes, and values, but also by how those facts are presented. Equivalent descriptions can lead to different judgments when frames shift reference points, gain-loss coding, salience, comparison sets, or perceived responsibility.

## Modeling Principles

1. Define the decision before selecting the frame.
2. Document the current frame and its implied reference point.
3. Present equivalent gain and loss frames side by side.
4. Compare absolute and relative risk formats.
5. Test whether the preferred action changes under equivalent descriptions.
6. Identify which values each frame highlights or hides.
7. Include stakeholder review when frames affect legitimacy or burden.
8. Flag frame-sensitive decisions for review.
9. Treat AI interfaces, dashboards, and labels as framing systems.
10. Preserve frames, reference points, assumptions, alternatives, and review triggers in decision records.

## Quick Start

From this article directory:

```bash
python3 python/run_all_framing_workflows.py
Rscript r/run_all_framing_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
