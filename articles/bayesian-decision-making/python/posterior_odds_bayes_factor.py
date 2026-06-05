#!/usr/bin/env python3
"""Posterior odds and Bayes factor helpers."""

from __future__ import annotations


def odds(probability: float) -> float:
    if probability >= 1.0:
        return float("inf")
    if probability <= 0.0:
        return 0.0
    return probability / (1.0 - probability)


def bayes_factor(likelihood_h: float, likelihood_not_h: float) -> float:
    if likelihood_not_h == 0:
        return float("inf")
    return likelihood_h / likelihood_not_h


if __name__ == "__main__":
    print(round(odds(0.443299), 6))
    print(round(bayes_factor(0.86, 0.12), 6))
