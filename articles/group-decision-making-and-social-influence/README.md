# Group Decision-Making and Social Influence

This companion directory supports the article **"Group Decision-Making and Social Influence."**

The workflows operationalize group decision-making as a reproducible decision-science problem involving independent judgment, social influence, authority weighting, consensus pressure, dissent, hidden-profile risk, information diversity, collective error, decision rules, review queues, and decision-record scaffolding.

## Core Claim

Group decision-making is not simply the aggregation of individual opinions. It is a social process that can improve judgment through diversity, expertise, dissent, and information pooling, or weaken judgment through conformity, authority bias, hidden profiles, premature consensus, groupthink, and polarization.

## Modeling Principles

1. Preserve independent judgments before discussion.
2. Distinguish informational influence from normative influence.
3. Separate shared information from unique information.
4. Track influence weights, authority concentration, and consensus pressure.
5. Record dissent before it disappears into group memory.
6. Detect hidden-profile risk where decision-critical evidence is unevenly distributed.
7. Compare independent group estimates with socially influenced group estimates.
8. Use decision rules that match stakes, uncertainty, reversibility, and legitimacy.
9. Treat participation, power, and representation as decision-quality concerns.
10. Preserve decision records for evidence, dissent, confidence, decision rules, selected action, and review triggers.

## Quick Start

From this article directory:

```bash
python3 python/run_all_group_decision_workflows.py
Rscript r/run_all_group_decision_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
