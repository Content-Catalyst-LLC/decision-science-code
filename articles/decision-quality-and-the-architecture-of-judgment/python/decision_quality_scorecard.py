#!/usr/bin/env python3
"""Decision quality scorecard helper."""

from __future__ import annotations


def weighted_score(scores: dict[str, float], weights: dict[str, float]) -> float:
    if abs(sum(weights.values()) - 1.0) > 1e-9:
        raise ValueError("Weights must sum to 1")
    return sum(scores[key] * weights[key] for key in weights)


if __name__ == "__main__":
    scores = {"framing": 0.88, "evidence": 0.82, "uncertainty": 0.91, "learning": 0.90}
    weights = {"framing": 0.25, "evidence": 0.25, "uncertainty": 0.25, "learning": 0.25}
    print(round(weighted_score(scores, weights), 4))
