# Adaptive Decision Pathways

This companion directory supports the article **"Adaptive Decision Pathways."**

The workflows operationalize adaptive decision pathways as a reproducible decision-science problem involving staged action, monitoring indicators, trigger points, fallback options, switching rules, option value, pathway robustness, scenario comparison, governance responsibilities, and decision-record scaffolding.

## Core Claim

Uncertainty does not always require delay. Decision-makers can act responsibly when they design choices that are monitorable, revisable, staged, and accountable over time. Adaptive pathways turn a decision into a structured sequence: act now, preserve options, monitor change, define triggers, and shift pathways when conditions require revision.

## Modeling Principles

1. Treat decisions as staged pathways rather than one-time choices.
2. Separate the initial action from future revision.
3. Define monitoring indicators before stress occurs.
4. Connect trigger points to decision authority.
5. Preserve fallback options and switching rules.
6. Evaluate option value, reversibility, and switching cost.
7. Test pathways across plausible futures.
8. Include stakeholder values, legitimacy, and distributional effects.
9. Build governance that can actually revise the pathway.
10. Preserve assumptions, triggers, alternatives, dissent, and revision history in decision records.

## Quick Start

From this article directory:

```bash
python3 python/run_all_adaptive_pathway_workflows.py
Rscript r/run_all_adaptive_pathway_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
