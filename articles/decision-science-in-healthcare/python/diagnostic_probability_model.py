#!/usr/bin/env python3
"""Diagnostic probability helper using Bayes' rule."""

from __future__ import annotations


def bayes_update(prior: float, sensitivity: float, specificity: float, positive: bool = True) -> float:
    if positive:
        numerator = sensitivity * prior
        denominator = sensitivity * prior + (1.0 - specificity) * (1.0 - prior)
    else:
        numerator = (1.0 - sensitivity) * prior
        denominator = (1.0 - sensitivity) * prior + specificity * (1.0 - prior)

    if denominator == 0:
        raise ValueError("Denominator is zero. Check probability inputs.")

    return numerator / denominator


if __name__ == "__main__":
    print(round(bayes_update(prior=0.10, sensitivity=0.90, specificity=0.85, positive=True), 6))
