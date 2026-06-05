# Decision Records and Accountable Judgment

This companion directory supports the article **"Decision Records and Accountable Judgment."**

The workflows operationalize decision records as tools for accountable judgment, institutional memory, assumption traceability, review triggers, dissent preservation, monitoring, and learning. The examples use synthetic but professionally structured data so the workflows can be adapted to policy, strategy, healthcare, finance, infrastructure, AI governance, and other high-stakes decisions.

## Core Claim

Decision records make judgment accountable by preserving the reasoning behind a choice before outcomes are known. They document what was decided, why it was decided, what evidence supported it, what remained uncertain, what assumptions mattered, what alternatives were rejected, what dissent existed, and what should trigger review.

## Modeling Principles

1. Define the decision before documenting analysis.
2. Preserve alternatives considered, rejected, deferred, and selected.
3. Link evidence to the claims it supports.
4. Make assumptions explicit, confidence-rated, and reviewable.
5. Represent uncertainty honestly rather than compressing it into false certainty.
6. Preserve values, criteria, weights, thresholds, and trade-offs.
7. Record credible dissent and unresolved disagreement.
8. Define monitoring indicators and review triggers.
9. Preserve decision records for accountability and institutional learning.
10. Treat computational models as supports for judgment, not replacements for responsibility.

## Quick Start

From this article directory:

```bash
python3 python/run_all_decision_record_workflows.py
Rscript r/run_all_decision_record_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
