#!/usr/bin/env python3
"""Human oversight capacity helper."""

from __future__ import annotations


def oversight_capacity(authority: float, information: float, time: float, expertise: float, independence: float) -> float:
    return (
        0.24 * authority
        + 0.22 * information
        + 0.18 * time
        + 0.20 * expertise
        + 0.16 * independence
    )


def oversight_requires_review(score: float, threshold: float = 0.60) -> bool:
    return score < threshold


if __name__ == "__main__":
    score = oversight_capacity(0.75, 0.68, 0.60, 0.72, 0.66)
    print(round(score, 6))
    print(oversight_requires_review(score))
