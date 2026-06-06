#!/usr/bin/env python3
"""Calibration error and Brier scoring helper."""

from __future__ import annotations


def brier_score(probability: float, outcome: int) -> float:
    if probability < 0 or probability > 1:
        raise ValueError("Probability must be between 0 and 1.")
    if outcome not in (0, 1):
        raise ValueError("Outcome must be 0 or 1.")
    return (probability - outcome) ** 2


if __name__ == "__main__":
    print(round(brier_score(0.72, 1), 6))
    print(round(brier_score(0.84, 0), 6))
