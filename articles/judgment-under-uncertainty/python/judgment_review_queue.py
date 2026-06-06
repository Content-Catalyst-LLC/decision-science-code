#!/usr/bin/env python3
"""Judgment review queue helper."""

from __future__ import annotations


def review_flag(brier_score: float, confidence_gap: float, anchor_distortion: float) -> str:
    if brier_score > 0.25 or abs(confidence_gap) > 0.15 or anchor_distortion > 0.15:
        return "review"
    return "acceptable"


if __name__ == "__main__":
    print(review_flag(0.30, 0.04, 0.10))
    print(review_flag(0.12, 0.05, 0.07))
