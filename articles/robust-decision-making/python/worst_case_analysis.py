#!/usr/bin/env python3
from __future__ import annotations

def worst_case(values: list[float]) -> float:
    if not values:
        raise ValueError("At least one value is required.")
    return min(values)

if __name__ == "__main__":
    print(round(worst_case([0.92, 0.43, 0.17, 0.29]), 6))
