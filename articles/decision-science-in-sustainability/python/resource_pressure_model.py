#!/usr/bin/env python3
"""Resource pressure and stock helper."""

from __future__ import annotations


def resource_next(resource_stock: float, extraction: float, regeneration: float) -> float:
    return max(0.0, resource_stock - extraction + regeneration)


def pressure_next(resource_pressure: float, policy_response: float, governance_delay: float, random_component: float = 0.60) -> float:
    return max(5.0, resource_pressure + random_component - 0.050 * policy_response + 0.030 * governance_delay)


if __name__ == "__main__":
    print(round(resource_next(100.0, 28.0, 13.2), 6))
    print(round(pressure_next(28.0, 8.0, 5.0), 6))
