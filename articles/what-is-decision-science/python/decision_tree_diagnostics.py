#!/usr/bin/env python3
"""Minimal decision-tree diagnostics for sequential choice."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ChanceBranch:
    name: str
    probability: float
    payoff: float


@dataclass
class DecisionOption:
    name: str
    branches: list[ChanceBranch] = field(default_factory=list)

    def expected_value(self) -> float:
        probability_total = sum(branch.probability for branch in self.branches)
        if abs(probability_total - 1.0) > 1e-8:
            raise ValueError(f"Probabilities for {self.name} sum to {probability_total}")
        return sum(branch.probability * branch.payoff for branch in self.branches)


def main() -> None:
    options = [
        DecisionOption("Act now", [
            ChanceBranch("favorable", 0.45, 110),
            ChanceBranch("neutral", 0.35, 45),
            ChanceBranch("adverse", 0.20, -35),
        ]),
        DecisionOption("Stage decision", [
            ChanceBranch("favorable", 0.45, 82),
            ChanceBranch("neutral", 0.35, 52),
            ChanceBranch("adverse", 0.20, 18),
        ]),
    ]

    for option in options:
        print(option.name, round(option.expected_value(), 3))


if __name__ == "__main__":
    main()
