#!/usr/bin/env python3
"""Bayesian risk update helper."""

from __future__ import annotations


def bayesian_update(prior: float, sensitivity: float, false_positive_rate: float) -> float:
    evidence_probability = sensitivity * prior + false_positive_rate * (1.0 - prior)
    if evidence_probability == 0:
        raise ValueError("Evidence probability is zero.")
    return (sensitivity * prior) / evidence_probability


if __name__ == "__main__":
    print(round(bayesian_update(0.10, 0.82, 0.12), 6))
