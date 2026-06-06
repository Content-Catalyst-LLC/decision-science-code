#!/usr/bin/env python3
"""Lock-in risk helper."""

from __future__ import annotations


def lock_in_risk(switching_cost: float, institutional_routine: float, network_dependence: float, option_value: float) -> float:
    return 0.42 * switching_cost + 0.28 * institutional_routine + 0.20 * network_dependence - 0.10 * option_value


if __name__ == "__main__":
    print(round(lock_in_risk(0.58, 0.62, 0.55, 0.40), 6))
