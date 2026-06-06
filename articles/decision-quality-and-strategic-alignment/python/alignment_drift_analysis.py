#!/usr/bin/env python3
"""Alignment drift helper."""

from __future__ import annotations


def strategic_drift(alignment_score: float) -> float:
    if alignment_score < 0 or alignment_score > 1:
        raise ValueError("Alignment score must be between 0 and 1.")
    return 1.0 - alignment_score


if __name__ == "__main__":
    print(round(strategic_drift(0.91), 6))
