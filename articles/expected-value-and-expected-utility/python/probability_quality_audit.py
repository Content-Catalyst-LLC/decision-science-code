#!/usr/bin/env python3
"""Probability quality audit helper."""

from __future__ import annotations


QUALITY_SCORES = {
    "high": 1.0,
    "medium": 0.65,
    "low": 0.35,
}


def probability_quality_score(quality_labels: list[str]) -> float:
    if not quality_labels:
        return 0.0
    return sum(QUALITY_SCORES.get(label.lower(), 0.0) for label in quality_labels) / len(quality_labels)


if __name__ == "__main__":
    print(round(probability_quality_score(["medium", "medium", "low"]), 4))
