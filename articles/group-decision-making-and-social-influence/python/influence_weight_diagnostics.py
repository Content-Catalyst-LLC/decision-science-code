#!/usr/bin/env python3
"""Influence-weight diagnostics."""

from __future__ import annotations


def normalize_weights(values: list[float]) -> list[float]:
    total = sum(values)
    if total <= 0:
        raise ValueError("Weight total must be positive.")
    return [value / total for value in values]


def influence_concentration(weights: list[float]) -> float:
    if not weights:
        raise ValueError("At least one weight is required.")
    return max(weights)


if __name__ == "__main__":
    weights = normalize_weights([0.72, 0.61, 0.80, 0.47, 0.69, 0.58, 0.84])
    print(round(influence_concentration(weights), 6))
