#!/usr/bin/env python3
"""Implementation drift helper."""

from __future__ import annotations


def drift_next(current_drift: float, feedback_quality: float, implementation_capacity: float, random_component: float = 0.40) -> float:
    return max(0.0, current_drift + random_component - 0.030 * feedback_quality - 0.020 * implementation_capacity)


if __name__ == "__main__":
    print(round(drift_next(6.0, 12.0, 22.0), 6))
