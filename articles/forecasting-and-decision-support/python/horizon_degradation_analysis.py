#!/usr/bin/env python3
"""Forecast horizon degradation helper."""

from __future__ import annotations


def horizon_confidence_adjustment(base_confidence: float, horizon_days: int) -> float:
    adjustment = min(0.35, horizon_days / 365.0 * 0.20)
    return max(0.0, base_confidence - adjustment)


if __name__ == "__main__":
    for horizon in [7, 30, 90, 180, 365]:
        print(horizon, round(horizon_confidence_adjustment(0.80, horizon), 6))
