#!/usr/bin/env python3
from __future__ import annotations

def max_regret(values: list[float], scenario_bests: list[float]) -> float:
    if len(values) != len(scenario_bests):
        raise ValueError("Values and scenario bests must have equal length.")
    return max(best - value for value, best in zip(values, scenario_bests))

if __name__ == "__main__":
    print(round(max_regret([0.7, 0.5, 0.8], [0.9, 0.7, 0.85]), 6))
