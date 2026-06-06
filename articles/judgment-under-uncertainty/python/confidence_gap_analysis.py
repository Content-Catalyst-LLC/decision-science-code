#!/usr/bin/env python3
"""Confidence-gap diagnostics."""

from __future__ import annotations


def confidence_gap(confidence: float, forecast_probability: float) -> float:
    return confidence - forecast_probability


def confidence_label(gap: float, tolerance: float = 0.10) -> str:
    if gap > tolerance:
        return "overconfident"
    if gap < -tolerance:
        return "underconfident"
    return "approximately calibrated"


if __name__ == "__main__":
    gap = confidence_gap(0.82, 0.69)
    print(round(gap, 6), confidence_label(gap))
