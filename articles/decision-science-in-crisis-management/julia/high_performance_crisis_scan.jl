function crisis_decision_score(expected_value, worst_case, dispersion, speed, feasibility, equity, trust, continuity, adaptability)
    return 0.22 * expected_value / 100 + 0.20 * worst_case / 100 - 0.08 * dispersion / 30 + 0.12 * speed + 0.10 * feasibility + 0.14 * equity + 0.12 * trust + 0.10 * continuity + 0.10 * adaptability
end

println("Crisis decision score = ", round(crisis_decision_score(80.6, 76.0, 4.0, 0.82, 0.72, 0.80, 0.82, 0.80, 0.90), digits=6))
