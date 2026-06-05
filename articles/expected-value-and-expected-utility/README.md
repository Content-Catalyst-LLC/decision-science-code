# Expected Value and Expected Utility

This companion directory supports the article **"Expected Value and Expected Utility."**

The workflows operationalize expected value, expected utility, utility functions, risk aversion, certainty equivalents, risk premiums, probability-quality auditing, sensitivity analysis, and decision-record documentation.

## Core Claim

Expected value and expected utility provide formal tools for reasoning under uncertainty, but they must be used carefully. Expected value is a risk-neutral probability-weighted benchmark. Expected utility incorporates risk attitude and subjective or institutional valuation through a utility function. Neither is an automatic answer machine. Both depend on the quality of outcomes, probabilities, preference assumptions, and decision context.

## Modeling Principles

1. Define the decision and alternatives before calculating expected value.
2. Make outcome states explicit.
3. Document probability sources, probability quality, and uncertainty.
4. Use expected value as a risk-neutral benchmark, not as a universal answer.
5. Use expected utility when risk attitude, downside exposure, or nonlinear valuation matters.
6. Document and justify utility functions.
7. Estimate certainty equivalents and risk premiums for interpretability.
8. Test sensitivity across probabilities, outcomes, and risk-aversion parameters.
9. Record model assumptions for accountability and learning.
10. Treat computational models as supports for judgment, not replacements for responsibility.

## Quick Start

From this article directory:

```bash
python3 python/run_all_expected_utility_workflows.py
Rscript r/run_all_expected_utility_workflows.R
```

Outputs are written to:

```text
outputs/tables/
outputs/figures/
outputs/decision_records/
```
