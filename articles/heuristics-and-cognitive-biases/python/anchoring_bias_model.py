#!/usr/bin/env python3
"""Anchoring-bias model."""

from __future__ import annotations


def anchored_estimate(anchor: float, evidence_estimate: float, anchor_weight: float = 0.45) -> float:
    if not 0 <= anchor_weight <= 1:
        raise ValueError("Anchor weight must be between 0 and 1.")
    return anchor_weight * anchor + (1 - anchor_weight) * evidence_estimate


if __name__ == "__main__":
    print(round(anchored_estimate(0.80, 0.42), 6))
