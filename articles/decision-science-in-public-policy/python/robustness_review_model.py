#!/usr/bin/env python3
"""Robustness review helper."""

from __future__ import annotations


def requires_robustness_review(worst_case_performance: float, threshold_pass_rate: float) -> bool:
    return worst_case_performance < 0.55 or threshold_pass_rate < 0.60


if __name__ == "__main__":
    print(requires_robustness_review(0.50, 0.40))
