#!/usr/bin/env python3
"""Model-risk review helper."""

from __future__ import annotations


def model_requires_review(model_confidence: float, governance_score: float, drift_score: float, threshold: float = 0.55) -> bool:
    return model_confidence < threshold or governance_score < threshold or drift_score > 0.45


if __name__ == "__main__":
    print(model_requires_review(model_confidence=0.52, governance_score=0.54, drift_score=0.30))
