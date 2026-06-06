#!/usr/bin/env python3
"""Confidence-error diagnostics."""

from __future__ import annotations


def confidence_error(confidence: float, accuracy_proxy: float) -> float:
    return confidence - accuracy_proxy


def confidence_flag(error: float, threshold: float = 0.15) -> str:
    if error > threshold:
        return "overconfident"
    if error < -threshold:
        return "underconfident"
    return "approximately calibrated"


if __name__ == "__main__":
    error = confidence_error(0.88, 0.52)
    print(round(error, 6), confidence_flag(error))
