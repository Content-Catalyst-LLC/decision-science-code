#!/usr/bin/env python3
"""Bayesian-style update diagnostics."""

from __future__ import annotations


def posterior_from_likelihoods(prior: float, likelihood_if_true: float, likelihood_if_false: float) -> float:
    if not 0 < prior < 1:
        raise ValueError("Prior must be between 0 and 1.")
    odds = prior / (1.0 - prior)
    posterior_odds = odds * (likelihood_if_true / likelihood_if_false)
    return posterior_odds / (1.0 + posterior_odds)


if __name__ == "__main__":
    print(round(posterior_from_likelihoods(0.35, 0.72, 0.28), 6))
