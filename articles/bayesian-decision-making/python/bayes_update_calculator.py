#!/usr/bin/env python3
"""Bayesian update calculator."""

from __future__ import annotations


def bayesian_update(prior: float, sensitivity: float, false_positive_rate: float) -> float:
    numerator = sensitivity * prior
    denominator = numerator + false_positive_rate * (1.0 - prior)
    if denominator == 0:
        raise ValueError("Evidence probability is zero.")
    return numerator / denominator


if __name__ == "__main__":
    print(round(bayesian_update(0.10, 0.86, 0.12), 6))
