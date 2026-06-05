#!/usr/bin/env python3
"""Confidence bias diagnostic helper."""

from __future__ import annotations


def confidence_bias_label(calibration_gap: float, tolerance: float = 0.05) -> str:
    if calibration_gap > tolerance:
        return "overconfident"
    if calibration_gap < -tolerance:
        return "underconfident"
    return "well calibrated"


if __name__ == "__main__":
    print(confidence_bias_label(0.12))
    print(confidence_bias_label(-0.09))
    print(confidence_bias_label(0.01))
