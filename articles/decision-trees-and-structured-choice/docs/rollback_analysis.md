# Rollback Analysis

Rollback analysis evaluates a decision tree from terminal nodes backward.

At chance nodes:
EV = sum(probability * value)

At decision nodes:
choose the branch with the best downstream value.

Rollback can use expected value, expected utility, regret, robustness, or another decision rule.
