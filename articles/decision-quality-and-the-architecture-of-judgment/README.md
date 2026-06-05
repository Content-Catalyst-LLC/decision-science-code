# Decision Quality and the Architecture of Judgment

This companion directory supports the article **"Decision Quality and the Architecture of Judgment."**

The workflows operationalize decision quality as a process standard distinct from outcome quality. They compare alternatives across framing, alternative quality, evidence, uncertainty treatment, trade-off clarity, behavioral safeguards, systems awareness, accountability, learning design, downside exposure, outcome bias, and review triggers.

## Core Claim

Decision quality is not the same as outcome quality. A good decision can produce a bad outcome under genuine uncertainty, and a weak decision process can produce a good outcome through luck. Decision science therefore evaluates the architecture of judgment before uncertainty resolves.

## Modeling Principles

1. Separate decision-process quality from realized outcome quality.
2. Evaluate framing, alternatives, evidence, uncertainty, trade-offs, behavioral safeguards, systems awareness, accountability, and learning.
3. Treat favorable outcomes from weak processes as possible luck.
4. Treat unfavorable outcomes from strong processes as opportunities for assumption review, not automatic blame.
5. Use sensitivity analysis to test dependence on quality-component weights.
6. Use simulation to distinguish process quality from outcome variance.
7. Preserve decision records to reduce hindsight bias and support institutional learning.
8. Treat computational models as supports for judgment, not replacements for responsibility.

## Quick Start

From this article directory:

```bash
python3 python/run_all_decision_quality_workflows.py
Rscript r/run_all_decision_quality_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
