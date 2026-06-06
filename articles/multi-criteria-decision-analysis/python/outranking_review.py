#!/usr/bin/env python3
"""Simple outranking helper."""

from __future__ import annotations


def concordance(scores_a: list[float], scores_b: list[float], weights: list[float]) -> float:
    if not (len(scores_a) == len(scores_b) == len(weights)):
        raise ValueError("Scores and weights must have equal length.")
    return sum(weight for a, b, weight in zip(scores_a, scores_b, weights) if a >= b)


if __name__ == "__main__":
    print(round(concordance([0.8, 0.5, 0.9], [0.7, 0.6, 0.8], [0.3, 0.3, 0.4]), 6))
