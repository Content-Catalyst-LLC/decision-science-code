# Behavioral Decision Theory

This companion directory supports the article **"Behavioral Decision Theory."**

The workflows operationalize behavioral decision theory as a reproducible decision-science problem involving expected utility, prospect theory, reference dependence, loss aversion, probability weighting, framing effects, rank divergence, behavioral review queues, choice architecture diagnostics, and decision-record scaffolding.

## Core Claim

Behavioral decision theory does not reject formal decision models. It shows where formal models need psychological realism, process safeguards, ethical constraints, and institutional design because real people and organizations decide under cognitive limits, emotional salience, social pressure, framing, uncertainty, and bounded rationality.

## Modeling Principles

1. Establish the formal decision benchmark before behavioral diagnosis.
2. Make reference points explicit.
3. Compare expected value, expected utility, and prospect-theory-style scores.
4. Test gain, loss, action, inaction, cost, investment, and avoided-loss frames.
5. Quantify probability-weighting distortion where risk perception matters.
6. Treat loss aversion and framing as decision-process risks.
7. Detect rank divergence between formal and behavioral scoring.
8. Use review queues for high-divergence, high-frame-sensitivity decisions.
9. Treat choice architecture as an ethical and governance issue.
10. Preserve behavioral decision records for assumptions, frames, reference points, bias checks, dissent, selected action, and learning.

## Quick Start

From this article directory:

```bash
python3 python/run_all_behavioral_decision_workflows.py
Rscript r/run_all_behavioral_decision_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
