#!/usr/bin/env python3
"""Classify process quality versus outcome quality."""

from __future__ import annotations


def classify(process_score: float, outcome: float, process_threshold: float = 0.80, outcome_threshold: float = 75.0) -> str:
    good_process = process_score >= process_threshold
    good_outcome = outcome >= outcome_threshold
    if good_process and good_outcome:
        return "good process and good outcome"
    if good_process and not good_outcome:
        return "good process exposed to unfavorable uncertainty"
    if not good_process and good_outcome:
        return "weak process with favorable outcome; possible luck"
    return "weak process and weak outcome"


if __name__ == "__main__":
    print(classify(0.86, 62.0))
    print(classify(0.52, 91.0))
