#!/usr/bin/env python3
"""Overconfidence review queue helper."""

from __future__ import annotations


def review_flag(
    confidence_error: float,
    brier_score: float,
    planning_error: float,
    interval_hit: bool,
) -> str:
    if confidence_error > 0.15 or brier_score > 0.25 or planning_error > 0.30 or not interval_hit:
        return "review"
    return "acceptable"


if __name__ == "__main__":
    print(review_flag(0.20, 0.10, 0.15, True))
    print(review_flag(0.05, 0.10, 0.15, True))
