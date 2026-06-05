#!/usr/bin/env python3
"""Probability quality audit helper."""

from __future__ import annotations

from statistics import mean

QUALITY_SCORES = {
    "high": 1.00,
    "medium": 0.65,
    "low": 0.35,
}


def probability_quality_score(labels: list[str]) -> float:
    if not labels:
        return 0.0
    return mean(QUALITY_SCORES.get(label.lower(), 0.0) for label in labels)


if __name__ == "__main__":
    print(round(probability_quality_score(["medium", "low", "high"]), 6))
