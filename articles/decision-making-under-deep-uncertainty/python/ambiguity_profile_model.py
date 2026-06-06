#!/usr/bin/env python3
"""Ambiguity profile helper."""

from __future__ import annotations


def validate_profile(weights: dict[str, float]) -> bool:
    return abs(sum(weights.values()) - 1.0) <= 1e-6 and all(value >= 0 for value in weights.values())


if __name__ == "__main__":
    print(validate_profile({"stable_growth": 0.2, "fiscal_stress": 0.3, "climate_disruption": 0.5}))
    print(validate_profile({"stable_growth": 0.2, "fiscal_stress": 0.3, "climate_disruption": 0.4}))
