#!/usr/bin/env python3
"""Decision hygiene review queue helper."""

from __future__ import annotations


def review_flag(post_absolute_error: float, post_brier_score: float, error_reduction: float, low_evidence_high_stakes: bool) -> str:
    if post_absolute_error > 0.15 or post_brier_score > 0.25 or error_reduction < 0 or low_evidence_high_stakes:
        return "review"
    return "acceptable"


if __name__ == "__main__":
    print(review_flag(0.16, 0.10, 0.04, False))
    print(review_flag(0.04, 0.10, 0.04, False))
