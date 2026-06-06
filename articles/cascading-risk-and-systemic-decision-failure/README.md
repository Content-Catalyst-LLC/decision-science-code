# Cascading Risk and Systemic Decision Failure

This companion directory supports the article **"Cascading Risk and Systemic Decision Failure."**

The workflows operationalize cascading risk as a reproducible decision-science problem involving dependency networks, threshold failure, systemic loss, buffer depletion, common-mode exposure, response capacity, early-warning indicators, scenario performance, containment planning, and decision-record scaffolding.

## Core Claim

Systemic failure often emerges when decision-makers underestimate interdependence, correlated exposure, feedback effects, threshold behavior, hidden dependencies, and the possibility that many actors will respond to stress at the same time. Cascading risk analysis shifts attention from isolated local failure to propagation pathways and system-level consequence.

## Modeling Principles

1. Treat risk as a networked, cross-system phenomenon.
2. Map dependencies before evaluating exposure.
3. Distinguish direct impact from propagation risk.
4. Test common-mode failure and correlated exposure.
5. Monitor buffers, recovery time, near misses, and threshold proximity.
6. Preserve redundancy, modularity, diversity, and graceful degradation where failure would propagate.
7. Connect early-warning indicators to escalation authority.
8. Use scenario tests to examine local disruption, common-mode shock, demand surge, and delayed response.
9. Document dependencies, assumptions, thresholds, containment plans, and dissent.
10. Treat systemic accountability as responsibility for consequences that cross ordinary boundaries.

## Quick Start

From this article directory:

```bash
python3 python/run_all_cascading_risk_workflows.py
Rscript r/run_all_cascading_risk_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
