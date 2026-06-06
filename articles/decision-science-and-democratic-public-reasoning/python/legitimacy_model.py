#!/usr/bin/env python3
"""Legitimacy helper for democratic public reasoning."""

from __future__ import annotations


def legitimacy_score(
    transparency: float,
    participation: float,
    procedural_fairness: float,
    evidence_quality: float,
    contestability: float,
    accountability: float,
) -> float:
    return (
        0.17 * transparency
        + 0.17 * participation
        + 0.18 * procedural_fairness
        + 0.16 * evidence_quality
        + 0.16 * contestability
        + 0.16 * accountability
    )


if __name__ == "__main__":
    print(round(legitimacy_score(0.88, 0.88, 0.88, 0.84, 0.86, 0.88), 6))
