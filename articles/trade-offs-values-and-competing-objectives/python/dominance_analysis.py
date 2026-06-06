#!/usr/bin/env python3
"""Dominance analysis helper."""

from __future__ import annotations


def is_dominated(a_scores: list[float], b_scores: list[float]) -> bool:
    if len(a_scores) != len(b_scores):
        raise ValueError("Score vectors must have same length.")
    return all(b >= a for a, b in zip(a_scores, b_scores)) and any(b > a for a, b in zip(a_scores, b_scores))


if __name__ == "__main__":
    print(is_dominated([0.5, 0.6, 0.7], [0.5, 0.7, 0.8]))
    print(is_dominated([0.9, 0.6, 0.7], [0.5, 0.7, 0.8]))
