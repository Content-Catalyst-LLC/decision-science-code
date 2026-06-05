#!/usr/bin/env python3
"""One-way sensitivity helper."""

from __future__ import annotations


def one_way_score(base: float, coefficient: float, value: float) -> float:
    return base + coefficient * value


if __name__ == "__main__":
    for value in [-1.0, 0.0, 1.0]:
        print(value, round(one_way_score(75.0, 8.0, value), 6))
