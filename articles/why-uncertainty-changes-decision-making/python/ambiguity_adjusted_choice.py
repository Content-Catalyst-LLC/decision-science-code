#!/usr/bin/env python3
"""Ambiguity-adjusted choice scaffold."""

from __future__ import annotations


def ambiguity_adjusted_score(expected_score: float, ambiguity_exposure: float, ambiguity_lambda: float) -> float:
    return expected_score - ambiguity_lambda * ambiguity_exposure


if __name__ == "__main__":
    strategies = {
        "Expand": (0.72, 0.42),
        "Hedge": (0.68, 0.22),
        "Preserve Option": (0.60, 0.08),
        "Adaptive Pathway": (0.70, 0.15),
    }
    scores = {name: ambiguity_adjusted_score(value, ambiguity, 1.5) for name, (value, ambiguity) in strategies.items()}
    print(scores)
    print("Selected:", max(scores, key=scores.get))
