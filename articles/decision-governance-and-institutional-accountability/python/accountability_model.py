#!/usr/bin/env python3
"""Accountability scoring helper."""

from __future__ import annotations


def accountability_score(
    decision_rights: float,
    evidence_traceability: float,
    review_strength: float,
    ownership: float,
    monitoring: float,
    corrective_capacity: float,
) -> float:
    return (
        0.18 * decision_rights
        + 0.17 * evidence_traceability
        + 0.18 * review_strength
        + 0.17 * ownership
        + 0.15 * monitoring
        + 0.15 * corrective_capacity
    )


if __name__ == "__main__":
    print(round(accountability_score(0.82, 0.86, 0.88, 0.84, 0.90, 0.92), 6))
