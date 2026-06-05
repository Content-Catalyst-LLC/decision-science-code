# Bayesian Decision-Making

This companion directory supports the article **"Bayesian Decision-Making."**

The workflows operationalize Bayesian decision-making as a reproducible decision-science practice. They include Bayesian updating, posterior odds, Bayes factors, posterior expected utility, prior sensitivity, sequential learning, value-of-information analysis, evidence-quality auditing, and decision-record scaffolding.

## Core Claim

Bayesian decision-making connects probability, evidence, learning, and action. It allows decision-makers to begin with incomplete knowledge, update beliefs as evidence arrives, and choose actions under posterior uncertainty. Its value is not only mathematical; it makes priors, likelihoods, evidence, posterior beliefs, utility assumptions, and review triggers explicit.

## Modeling Principles

1. Define the uncertain state before updating probabilities.
2. Document the prior and its source.
3. Distinguish likelihood from posterior probability.
4. Assess evidence quality before treating signals as diagnostic.
5. Use posterior beliefs for action selection.
6. Compare actions using posterior expected utility, expected loss, or thresholds.
7. Run prior and likelihood sensitivity analysis.
8. Use sequential learning when evidence arrives over time.
9. Define review triggers tied to posterior thresholds and utility sensitivity.
10. Treat Bayesian models as supports for judgment, not replacements for responsibility.

## Quick Start

From this article directory:

```bash
python3 python/run_all_bayesian_workflows.py
Rscript r/run_all_bayesian_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
