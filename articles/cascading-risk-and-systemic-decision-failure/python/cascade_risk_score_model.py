#!/usr/bin/env python3
"""Cascade risk score helper."""

from __future__ import annotations


def cascade_risk_score(
    exposure: float,
    dependency_centrality: float,
    buffer_weakness: float,
    common_mode_risk: float,
    monitoring_quality: float,
    response_capacity: float,
) -> float:
    return (
        0.22 * exposure
        + 0.22 * dependency_centrality
        + 0.20 * buffer_weakness
        + 0.18 * common_mode_risk
        - 0.09 * monitoring_quality
        - 0.09 * response_capacity
    )


if __name__ == "__main__":
    print(round(cascade_risk_score(0.82, 0.88, 0.76, 0.79, 0.42, 0.40), 6))
