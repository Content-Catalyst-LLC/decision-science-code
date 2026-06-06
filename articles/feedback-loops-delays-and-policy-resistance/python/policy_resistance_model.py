#!/usr/bin/env python3
"""Policy resistance helper."""

from __future__ import annotations


def net_policy_effect(policy_delta: float, intended_strength: float, resistance_strength: float, resistance_response: float) -> float:
    return intended_strength * policy_delta - resistance_strength * resistance_response


if __name__ == "__main__":
    print(round(net_policy_effect(10.0, 0.8, 0.4, 6.0), 6))
