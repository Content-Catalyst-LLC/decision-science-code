#!/usr/bin/env python3
"""Bayesian update example for historical decision-science workflows."""

from __future__ import annotations


def posterior(prior: float, likelihood_if_true: float, likelihood_if_false: float) -> float:
    numerator = likelihood_if_true * prior
    denominator = numerator + likelihood_if_false * (1.0 - prior)
    if denominator == 0:
        raise ValueError("Invalid prior/likelihood combination")
    return numerator / denominator


if __name__ == "__main__":
    print(round(posterior(0.30, 0.75, 0.25), 4))
