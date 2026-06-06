#!/usr/bin/env python3
"""Behavioral review queue helper."""

from __future__ import annotations


def review_flag(rank_divergence: float, frame_sensitivity_index: float, probability_weight_distortion: float) -> str:
    if abs(rank_divergence) > 25 or frame_sensitivity_index > 100 or probability_weight_distortion > 0.12:
        return "review"
    return "acceptable"


if __name__ == "__main__":
    print(review_flag(30, 40, 0.03))
    print(review_flag(5, 20, 0.04))
