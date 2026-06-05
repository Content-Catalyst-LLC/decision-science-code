#!/usr/bin/env python3
"""Bayesian update and posterior expected-loss decision rule."""

from __future__ import annotations


def posterior(prior: float, likelihood_if_true: float, likelihood_if_false: float) -> float:
    numerator = likelihood_if_true * prior
    denominator = numerator + likelihood_if_false * (1.0 - prior)
    if denominator == 0:
        raise ValueError("Invalid likelihood/prior combination")
    return numerator / denominator


def expected_loss(false_positive_cost: float, false_negative_cost: float, posterior_risk: float) -> dict[str, float]:
    return {
        "act": false_positive_cost * (1.0 - posterior_risk),
        "do_not_act": false_negative_cost * posterior_risk,
    }


if __name__ == "__main__":
    p = posterior(prior=0.30, likelihood_if_true=0.80, likelihood_if_false=0.25)
    losses = expected_loss(false_positive_cost=25, false_negative_cost=80, posterior_risk=p)
    print("Posterior risk:", round(p, 4))
    print("Expected losses:", losses)
    print("Recommended action:", min(losses, key=losses.get))
