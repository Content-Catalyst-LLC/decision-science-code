#!/usr/bin/env python3
"""Post-decision learning loop helper."""

from __future__ import annotations


def update_belief(prior: float, evidence_strength: float, learning_rate: float = 0.35) -> float:
    return max(0.0, min(1.0, prior + learning_rate * (evidence_strength - prior)))


if __name__ == "__main__":
    print(round(update_belief(0.62, 0.40), 4))
    print(round(update_belief(0.62, 0.82), 4))
