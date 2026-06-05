#!/usr/bin/env python3
"""Multi-way sensitivity helper."""

from __future__ import annotations


def multi_way_score(base: float, demand: float, cost: float, disruption: float) -> float:
    return base + 8.0 * demand - 10.0 * cost - 11.0 * disruption


if __name__ == "__main__":
    print(round(multi_way_score(75.0, 0.5, 0.3, 0.2), 6))
    print(round(multi_way_score(75.0, -0.5, 1.1, 1.4), 6))
