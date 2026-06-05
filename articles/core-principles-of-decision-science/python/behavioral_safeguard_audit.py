#!/usr/bin/env python3
"""Behavioral safeguard audit."""

from __future__ import annotations


def safeguard_score(independent_estimates: bool, premortem: bool, red_team: bool, calibration: bool, dissent_recorded: bool) -> float:
    return sum([independent_estimates, premortem, red_team, calibration, dissent_recorded]) / 5.0


if __name__ == "__main__":
    print(safeguard_score(True, True, False, True, True))
