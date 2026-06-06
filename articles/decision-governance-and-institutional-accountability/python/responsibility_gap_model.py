#!/usr/bin/env python3
"""Responsibility gap helper."""

from __future__ import annotations


def responsibility_gap(decision_influence: float, accountability: float) -> float:
    return max(0.0, decision_influence - accountability)


def gap_requires_review(gap: float, threshold: float = 0.28) -> bool:
    return gap >= threshold


if __name__ == "__main__":
    gap = responsibility_gap(0.62, 0.34)
    print(round(gap, 6))
    print(gap_requires_review(gap))
