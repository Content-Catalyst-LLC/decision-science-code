#!/usr/bin/env python3
"""Small luck-versus-skill simulation."""

from __future__ import annotations

import random
from statistics import mean


def simulate(process_quality: float, trials: int = 200, seed: int = 7) -> float:
    rng = random.Random(seed)
    outcomes = []
    for _ in range(trials):
        luck = rng.gauss(0, 25)
        outcome = 55 + 45 * process_quality + luck
        outcomes.append(outcome >= 75)
    return sum(1 for item in outcomes if item) / len(outcomes)


if __name__ == "__main__":
    print(round(simulate(0.40), 4))
    print(round(simulate(0.85), 4))
