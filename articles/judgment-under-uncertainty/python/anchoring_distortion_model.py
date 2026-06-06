#!/usr/bin/env python3
"""Anchoring distortion model."""

from __future__ import annotations


def anchor_adjusted_judgment(anchor: float, evidence_estimate: float, anchor_weight: float) -> float:
    return max(0.01, min(0.99, anchor_weight * anchor + (1.0 - anchor_weight) * evidence_estimate))


def anchor_distortion(anchor_adjusted: float, evidence_estimate: float) -> float:
    return abs(anchor_adjusted - evidence_estimate)


if __name__ == "__main__":
    adjusted = anchor_adjusted_judgment(0.70, 0.42, 0.48)
    print(round(adjusted, 6), round(anchor_distortion(adjusted, 0.42), 6))
