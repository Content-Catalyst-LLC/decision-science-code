#!/usr/bin/env python3
"""Infrastructure alternative value helper."""

from __future__ import annotations


def expected_service_value(values: dict[str, float], probabilities: dict[str, float]) -> float:
    return sum(values[name] * probabilities[name] for name in values)


def worst_case_value(values: dict[str, float]) -> float:
    return min(values.values())


if __name__ == "__main__":
    values = {"baseline": 76.0, "climate_stress": 76.0, "demand_growth": 82.0, "funding_constraint": 70.0, "disruption": 78.0}
    probabilities = {"baseline": 0.30, "climate_stress": 0.20, "demand_growth": 0.20, "funding_constraint": 0.15, "disruption": 0.15}
    print(round(expected_service_value(values, probabilities), 6))
    print(round(worst_case_value(values), 6))
