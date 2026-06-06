#!/usr/bin/env python3
"""Framing review-queue helper."""

from __future__ import annotations


def review_flag(frame_reversal: bool, frame_sensitivity_index: float, threshold: float = 120.0) -> str:
    if frame_reversal or frame_sensitivity_index >= threshold:
        return "review"
    return "acceptable"


if __name__ == "__main__":
    print(review_flag(True, 20.0))
    print(review_flag(False, 150.0))
