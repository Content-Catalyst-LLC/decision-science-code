#!/usr/bin/env python3
"""Debiasing review-queue helper."""

from __future__ import annotations


def review_flag(bias_magnitude: float, confidence_gap: float, brier_score: float) -> str:
    if bias_magnitude > 0.12 or abs(confidence_gap) > 0.12 or brier_score > 0.25:
        return "review"
    return "acceptable"


if __name__ == "__main__":
    print(review_flag(0.15, 0.04, 0.18))
    print(review_flag(0.05, 0.03, 0.10))
