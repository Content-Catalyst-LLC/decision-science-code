#!/usr/bin/env python3
"""Probabilistic sensitivity mini-example."""

from __future__ import annotations

import random
from statistics import mean


def main() -> None:
    rng = random.Random(42)
    values = []

    for _ in range(1000):
        demand = rng.uniform(-1.0, 2.0)
        cost = rng.uniform(0.0, 1.2)
        disruption = rng.uniform(0.0, 1.5)
        values.append(75.0 + 8.0 * demand - 10.0 * cost - 11.0 * disruption)

    print(round(mean(values), 6))
    print(round(min(values), 6))
    print(round(max(values), 6))


if __name__ == "__main__":
    main()
