#!/usr/bin/env python3
"""Prior sensitivity analysis helper."""

from __future__ import annotations


def bayesian_update(prior: float, sensitivity: float, false_positive_rate: float) -> float:
    numerator = sensitivity * prior
    denominator = numerator + false_positive_rate * (1.0 - prior)
    return numerator / denominator


if __name__ == "__main__":
    for prior in [0.05, 0.10, 0.25, 0.50]:
        print(prior, round(bayesian_update(prior, 0.86, 0.12), 6))
