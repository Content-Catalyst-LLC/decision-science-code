#!/usr/bin/env python3
"""Confidence distortion helper."""

from __future__ import annotations


def confidence_gap(confidence: float, judged_probability: float) -> float:
    return confidence - judged_probability


def confidence_label(gap: float, tolerance: float = 0.10) -> str:
    if gap > tolerance:
        return "overconfident"
    if gap < -tolerance:
        return "underconfident"
    return "calibrated enough for review"


if __name__ == "__main__":
    gap = confidence_gap(0.75, 0.60)
    print(round(gap, 6), confidence_label(gap))
