#!/usr/bin/env python3
"""Infrastructure resilience score helper."""

from __future__ import annotations


def resilience_score(condition: float, redundancy: float, adaptability: float, recovery_capacity: float, hazard_exposure: float) -> float:
    return max(
        0.0,
        min(
            1.0,
            0.28 * condition / 100.0
            + 0.22 * redundancy
            + 0.22 * adaptability
            + 0.18 * recovery_capacity
            - 0.10 * hazard_exposure,
        ),
    )


if __name__ == "__main__":
    print(round(resilience_score(76.0, 0.70, 0.90, 0.82, 0.58), 6))
