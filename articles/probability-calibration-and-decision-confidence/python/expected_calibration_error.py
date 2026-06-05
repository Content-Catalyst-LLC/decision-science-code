#!/usr/bin/env python3
"""Expected calibration error helper."""

from __future__ import annotations


def expected_calibration_error(weighted_gaps: list[float]) -> float:
    return sum(abs(value) for value in weighted_gaps)


if __name__ == "__main__":
    print(round(expected_calibration_error([0.01, 0.025, 0.015]), 6))
