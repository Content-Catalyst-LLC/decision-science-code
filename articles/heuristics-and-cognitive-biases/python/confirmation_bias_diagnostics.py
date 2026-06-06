#!/usr/bin/env python3
"""Confirmation-bias evidence-weighting diagnostic."""

from __future__ import annotations


def biased_evidence_update(prior: float, confirming: float, disconfirming: float, confirming_weight: float = 0.80, disconfirming_weight: float = 0.35) -> float:
    return max(0.01, min(0.99, prior + confirming_weight * confirming - disconfirming_weight * disconfirming))


if __name__ == "__main__":
    print(round(biased_evidence_update(0.46, 0.24, 0.06), 6))
