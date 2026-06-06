#!/usr/bin/env python3
"""Strategic alignment scoring helper."""

from __future__ import annotations

import math


def cosine_similarity(a: list[float], b: list[float]) -> float:
    if len(a) != len(b):
        raise ValueError("Vectors must have equal length.")
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


if __name__ == "__main__":
    print(round(cosine_similarity([0.2, 0.3, 0.5], [0.2, 0.25, 0.55]), 6))
