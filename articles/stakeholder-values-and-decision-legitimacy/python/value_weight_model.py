#!/usr/bin/env python3
"""Value weight model helper."""

from __future__ import annotations


def weighted_score(values: list[float], weights: list[float]) -> float:
    if len(values) != len(weights):
        raise ValueError("Values and weights must have the same length.")
    if abs(sum(weights) - 1.0) > 1e-9:
        raise ValueError("Weights must sum to 1.")
    return sum(value * weight for value, weight in zip(values, weights))


if __name__ == "__main__":
    print(round(weighted_score([0.7, 0.8, 0.9], [0.2, 0.3, 0.5]), 6))
