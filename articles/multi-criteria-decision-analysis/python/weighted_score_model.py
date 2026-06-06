#!/usr/bin/env python3
"""Weighted score helper."""

from __future__ import annotations


def weighted_score(scores: list[float], weights: list[float]) -> float:
    if len(scores) != len(weights):
        raise ValueError("Scores and weights must have the same length.")
    if abs(sum(weights) - 1.0) > 1e-9:
        raise ValueError("Weights must sum to 1.")
    return sum(score * weight for score, weight in zip(scores, weights))


if __name__ == "__main__":
    print(round(weighted_score([0.8, 0.6, 0.9], [0.3, 0.3, 0.4]), 6))
