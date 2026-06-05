#!/usr/bin/env python3
"""Trade-off weight sensitivity example."""

from __future__ import annotations


def weighted_score(values: dict[str, float], weights: dict[str, float]) -> float:
    if abs(sum(weights.values()) - 1.0) > 1e-9:
        raise ValueError("Weights must sum to 1")
    return sum(values[key] * weights[key] for key in weights)


if __name__ == "__main__":
    values = {"robustness": 0.86, "adaptability": 0.93, "evidence": 0.84}
    weights = {"robustness": 0.40, "adaptability": 0.40, "evidence": 0.20}
    print(round(weighted_score(values, weights), 4))
