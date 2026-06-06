#!/usr/bin/env python3
"""Assumption drift helper."""

from __future__ import annotations


def drift_next(current_drift: float, signal_pressure: float, adaptability: float, governance_support: float) -> float:
    return max(0.0, min(1.0, current_drift + signal_pressure - 0.025 * adaptability - 0.015 * governance_support))


def drift_requires_review(drift: float, trigger: float = 0.35) -> bool:
    return drift > trigger


if __name__ == "__main__":
    d = drift_next(0.20, 0.08, 0.42, 0.78)
    print(round(d, 6))
    print(drift_requires_review(d))
