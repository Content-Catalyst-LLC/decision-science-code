#!/usr/bin/env python3
"""Noisy expected-value choice model."""

from __future__ import annotations

import random


def noisy_choice(scores: dict[str, float], rng: random.Random, noise_scale: float = 8.0) -> str:
    noisy_scores = {name: value + rng.gauss(0, noise_scale) for name, value in scores.items()}
    return max(noisy_scores, key=noisy_scores.get)


if __name__ == "__main__":
    rng = random.Random(42)
    print(noisy_choice({"Aggressive": 49.4, "Balanced": 65.0, "Defensive": 56.8, "Adaptive": 70.2}, rng))
