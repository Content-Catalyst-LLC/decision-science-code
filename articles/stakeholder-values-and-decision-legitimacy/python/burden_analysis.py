#!/usr/bin/env python3
"""Burden analysis helper."""

from __future__ import annotations


def maximum_burden(values: list[float]) -> float:
    if not values:
        raise ValueError("At least one burden value is required.")
    return max(values)


if __name__ == "__main__":
    print(round(maximum_burden([0.18, 0.20, 0.26, 0.18, 0.22]), 6))
