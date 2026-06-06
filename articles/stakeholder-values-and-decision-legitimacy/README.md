# Stakeholder Values and Decision Legitimacy

This companion directory supports the article **"Stakeholder Values and Decision Legitimacy."**

The workflows operationalize stakeholder legitimacy as a reproducible decision-science problem involving stakeholder mapping, value weights, multi-criteria comparison, burden analysis, procedural legitimacy, threshold checks, decision-legitimacy scoring, dissent documentation, and decision-record scaffolding.

## Core Claim

Decision legitimacy is not created by technical analysis alone. Decisions become defensible when stakeholder values, affectedness, burdens, trade-offs, evidence, dissent, procedural safeguards, and accountability mechanisms are explicit enough to inspect, challenge, and revise.

## Modeling Principles

1. Separate stakeholder values from preferences and interests.
2. Map affectedness separately from influence.
3. Translate stakeholder values into criteria, thresholds, and constraints.
4. Compare alternatives across multiple stakeholder value profiles.
5. Track concentrated burden rather than relying only on aggregate benefit.
6. Evaluate procedural legitimacy: voice, transparency, explanation, contestability, and review.
7. Preserve dissent and contested assumptions.
8. Use thresholds to prevent unacceptable outcomes from being averaged away.
9. Treat legitimacy scores as diagnostics, not moral closure.
10. Preserve decision records before hindsight rewrites the rationale.

## Quick Start

From this article directory:

```bash
python3 python/run_all_stakeholder_legitimacy_workflows.py
Rscript r/run_all_stakeholder_legitimacy_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
