#!/usr/bin/env python3
"""Model-overconfidence check helpers."""

from __future__ import annotations


def model_confidence_review(
    calibration_gap: float,
    drift: float,
    subgroup_error_gap: float,
    threshold: float = 0.10,
) -> str:
    if abs(calibration_gap) > threshold or drift > threshold or subgroup_error_gap > threshold:
        return "review"
    return "acceptable"


if __name__ == "__main__":
    print(model_confidence_review(0.12, 0.03, 0.05))
    print(model_confidence_review(0.04, 0.03, 0.05))
