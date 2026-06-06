#!/usr/bin/env python3
"""AI drift trigger helper."""

from __future__ import annotations


def drift_indicator(current_metric: float, baseline_metric: float) -> float:
    return abs(current_metric - baseline_metric)


def drift_requires_review(current_metric: float, baseline_metric: float, threshold: float = 0.08) -> bool:
    return drift_indicator(current_metric, baseline_metric) >= threshold


if __name__ == "__main__":
    d = drift_indicator(0.77, 0.86)
    print(round(d, 6))
    print(drift_requires_review(0.77, 0.86))
