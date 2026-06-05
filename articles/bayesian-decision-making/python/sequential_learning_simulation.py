#!/usr/bin/env python3
"""Sequential Bayesian learning helper."""

from __future__ import annotations


def update_positive(prior: float, sensitivity: float, false_positive_rate: float) -> float:
    return (sensitivity * prior) / (sensitivity * prior + false_positive_rate * (1.0 - prior))


def update_negative(prior: float, sensitivity: float, false_positive_rate: float) -> float:
    likelihood_negative_h = 1.0 - sensitivity
    likelihood_negative_not_h = 1.0 - false_positive_rate
    return (likelihood_negative_h * prior) / (
        likelihood_negative_h * prior + likelihood_negative_not_h * (1.0 - prior)
    )


if __name__ == "__main__":
    posterior = 0.10
    for signal in ["positive", "positive", "negative"]:
        posterior = update_positive(posterior, 0.86, 0.12) if signal == "positive" else update_negative(posterior, 0.86, 0.12)
        print(signal, round(posterior, 6))
