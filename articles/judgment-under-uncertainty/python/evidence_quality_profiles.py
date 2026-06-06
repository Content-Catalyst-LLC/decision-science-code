#!/usr/bin/env python3
"""Evidence quality profile helper."""

from __future__ import annotations


def evidence_noise_sigma(evidence_quality: str) -> float:
    if evidence_quality == "high":
        return 0.03
    if evidence_quality == "medium":
        return 0.07
    if evidence_quality == "low":
        return 0.12
    raise ValueError("Evidence quality must be low, medium, or high.")


if __name__ == "__main__":
    for label in ["low", "medium", "high"]:
        print(label, evidence_noise_sigma(label))
