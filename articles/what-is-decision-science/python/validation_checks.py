#!/usr/bin/env python3
"""Validation checks for decision-science workflows."""

from __future__ import annotations

import math


def validate_probability_vector(probabilities: list[float]) -> None:
    if any(p < 0 for p in probabilities):
        raise ValueError("Probabilities cannot be negative")
    if not math.isclose(sum(probabilities), 1.0, abs_tol=1e-8):
        raise ValueError(f"Probabilities must sum to 1. Current sum: {sum(probabilities)}")


def validate_weights(weights: list[float]) -> None:
    if any(w < 0 for w in weights):
        raise ValueError("Weights cannot be negative")
    if not math.isclose(sum(weights), 1.0, abs_tol=1e-8):
        raise ValueError(f"Weights must sum to 1. Current sum: {sum(weights)}")


if __name__ == "__main__":
    validate_probability_vector([0.25, 0.25, 0.50])
    validate_weights([0.30, 0.40, 0.30])
    print("Validation checks passed.")
