# Multi-Criteria Decision Analysis

This companion directory supports the article **"Multi-Criteria Decision Analysis."**

The workflows operationalize MCDA as a reproducible decision-science problem involving criteria design, score normalization, weighted scoring, value trade-offs, stakeholder weight profiles, sensitivity analysis, rank stability, review flags, and decision-record scaffolding.

## Core Claim

Multi-Criteria Decision Analysis helps decision-makers compare alternatives when several important criteria must be considered at the same time. Its value is not merely the final ranking. Its value is the discipline it imposes on judgment: defining criteria, documenting weights, scoring alternatives, making trade-offs explicit, testing sensitivity, and preserving decision records.

## Modeling Principles

1. Define the decision before building the matrix.
2. Generate alternatives before scoring or weighting them.
3. Design criteria that represent objectives, stakeholder concerns, risks, and trade-offs.
4. Normalize scores so different units can be compared transparently.
5. Treat weights as value judgments, not purely technical parameters.
6. Test rankings under changing weights, scores, thresholds, and stakeholder profiles.
7. Use non-compensatory logic where minimum standards matter.
8. Report rank stability, not only final rank.
9. Preserve decision records for criteria, scores, weights, assumptions, dissent, and review triggers.
10. Treat MCDA as a decision aid, not an answer machine.

## Quick Start

From this article directory:

```bash
python3 python/run_all_mcda_workflows.py
Rscript r/run_all_mcda_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
