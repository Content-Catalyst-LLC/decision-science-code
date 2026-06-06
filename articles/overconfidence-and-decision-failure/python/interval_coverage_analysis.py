#!/usr/bin/env python3
"""Interval coverage diagnostics."""

from __future__ import annotations


def interval_hit(lower: float, upper: float, actual: float) -> bool:
    return lower <= actual <= upper


def coverage_rate(hits: list[bool]) -> float:
    if not hits:
        raise ValueError("At least one interval hit value is required.")
    return sum(1 for hit in hits if hit) / len(hits)


if __name__ == "__main__":
    hits = [interval_hit(90, 150, 154), interval_hit(70, 110, 96)]
    print(hits, round(coverage_rate(hits), 6))
