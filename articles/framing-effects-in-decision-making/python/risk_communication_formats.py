#!/usr/bin/env python3
"""Risk-communication format helper."""

from __future__ import annotations


def absolute_change(baseline: float, new_value: float) -> float:
    return new_value - baseline


def relative_change(baseline: float, new_value: float) -> float:
    if baseline == 0:
        return 0.0
    return (new_value - baseline) / baseline


if __name__ == "__main__":
    print(round(absolute_change(0.10, 0.07), 6))
    print(round(relative_change(0.10, 0.07), 6))
