#!/usr/bin/env python3
"""Scenario stress testing helper."""

from __future__ import annotations


def expected_stress_return(mean_return: float, shock_probability: float, shock_size: float, recovery_credit: float) -> float:
    return mean_return + shock_probability * shock_size + recovery_credit


if __name__ == "__main__":
    print(round(expected_stress_return(0.065, 0.025, -0.125, 0.015), 6))
