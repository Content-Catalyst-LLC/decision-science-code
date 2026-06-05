#!/usr/bin/env python3
"""Outcome-bias diagnostic helper."""

from __future__ import annotations


def outcome_bias_warning(process_score: float, favorable_outcome_rate: float) -> str:
    if process_score < 0.60 and favorable_outcome_rate > 0.50:
        return "possible luck masking weak process"
    if process_score >= 0.80 and favorable_outcome_rate < 0.50:
        return "sound process exposed to unfavorable uncertainty"
    return "process and outcome broadly aligned"


if __name__ == "__main__":
    print(outcome_bias_warning(0.52, 0.71))
    print(outcome_bias_warning(0.86, 0.42))
