#!/usr/bin/env python3
"""Stakeholder weight profile helper."""

from __future__ import annotations


def validate_weight_profile(weights: dict[str, float]) -> bool:
    return abs(sum(weights.values()) - 1.0) <= 1e-9 and all(value >= 0 for value in weights.values())


if __name__ == "__main__":
    print(validate_weight_profile({"cost": 0.3, "equity": 0.4, "resilience": 0.3}))
    print(validate_weight_profile({"cost": 0.3, "equity": 0.4, "resilience": 0.2}))
