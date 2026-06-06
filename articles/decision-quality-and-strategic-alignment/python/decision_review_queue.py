#!/usr/bin/env python3
"""Decision quality and alignment review queue helper."""

from __future__ import annotations


def review_flag(decision_quality: float, strategic_alignment: float, vector_alignment: float, implementation_readiness: float) -> str:
    if decision_quality < 0.70 or strategic_alignment < 0.70 or vector_alignment < 0.85 or implementation_readiness < 0.65:
        return "review"
    return "acceptable"


if __name__ == "__main__":
    print(review_flag(0.60, 0.80, 0.90, 0.80))
    print(review_flag(0.82, 0.88, 0.91, 0.77))
