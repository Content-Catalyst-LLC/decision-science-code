#!/usr/bin/env python3
"""Contestability helper."""

from __future__ import annotations


def contestability_score(
    evidence_challenge: float,
    assumption_challenge: float,
    review_capacity: float,
    stakeholder_standing: float,
) -> float:
    return 0.25 * evidence_challenge + 0.25 * assumption_challenge + 0.25 * review_capacity + 0.25 * stakeholder_standing


if __name__ == "__main__":
    print(round(contestability_score(0.82, 0.80, 0.86, 0.84), 6))
