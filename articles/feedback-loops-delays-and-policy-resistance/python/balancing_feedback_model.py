#!/usr/bin/env python3
"""Balancing feedback helper."""

from __future__ import annotations


def balancing_effect(policy_signal: float, correction_rate: float) -> float:
    return policy_signal * correction_rate


if __name__ == "__main__":
    print(round(balancing_effect(8.0, 0.14), 6))
