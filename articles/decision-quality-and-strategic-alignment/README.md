# Decision Quality and Strategic Alignment

This companion directory supports the article **"Decision Quality and Strategic Alignment."**

The workflows operationalize decision quality and strategic alignment as a reproducible decision-science problem involving process quality, strategic fit, implementation readiness, alignment drift, adaptive performance, review queues, and decision-record scaffolding.

## Core Claim

Decision quality asks whether a choice was constructed through a disciplined process before its outcome is known. Strategic alignment asks whether the choice supports the larger strategic logic the organization claims to pursue. Decision quality without alignment can produce elegant irrelevance; alignment without decision quality can produce coherent failure.

## Modeling Principles

1. Evaluate decision process separately from outcome quality.
2. Translate strategic priorities into operational decision criteria.
3. Compare meaningful alternatives before selecting a path.
4. Make trade-offs and uncertainty explicit.
5. Test strategic fit against mission, priorities, capabilities, values, time horizon, and operating model.
6. Separate implementation readiness from analytical attractiveness.
7. Use decision hygiene to reduce bias, overconfidence, groupthink, and false alignment.
8. Monitor alignment drift across repeated decisions.
9. Preserve decision records before outcomes create hindsight distortion.
10. Use feedback to update strategy, decision criteria, governance, and learning loops.

## Quick Start

From this article directory:

```bash
python3 python/run_all_decision_quality_alignment_workflows.py
Rscript r/run_all_decision_quality_alignment_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
