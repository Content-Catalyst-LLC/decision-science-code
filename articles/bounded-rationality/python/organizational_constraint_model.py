#!/usr/bin/env python3
"""Organizational constraint model."""

from __future__ import annotations


def constrained_utility(raw_utility: float, implementation_risk: float, information_silo_penalty: float, time_pressure_penalty: float) -> float:
    return max(0.0, raw_utility - implementation_risk - information_silo_penalty - time_pressure_penalty)


if __name__ == "__main__":
    print(round(constrained_utility(0.86, 0.12, 0.04, 0.03), 6))
