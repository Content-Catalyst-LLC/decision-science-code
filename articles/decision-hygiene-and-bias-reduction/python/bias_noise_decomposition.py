#!/usr/bin/env python3
"""Bias and noise decomposition helpers."""

from __future__ import annotations

from statistics import mean, stdev


def bias(errors: list[float]) -> float:
    if not errors:
        raise ValueError("At least one error is required.")
    return mean(errors)


def noise(errors: list[float]) -> float:
    if len(errors) < 2:
        return 0.0
    return stdev(errors)


def mse(errors: list[float]) -> float:
    if not errors:
        raise ValueError("At least one error is required.")
    return mean(error ** 2 for error in errors)


if __name__ == "__main__":
    sample_errors = [0.12, 0.04, -0.03, 0.08]
    print(round(bias(sample_errors), 6))
    print(round(noise(sample_errors), 6))
    print(round(mse(sample_errors), 6))
