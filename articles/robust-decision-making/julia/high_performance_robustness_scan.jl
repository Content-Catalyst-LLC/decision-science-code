function robustness_score(worst_case, pass_rate, max_regret, expected_value, performance_range)
    return 0.30 * worst_case + 0.25 * pass_rate + 0.20 * (1 - max_regret) + 0.15 * expected_value + 0.10 * (1 - performance_range)
end
println("Robustness score = ", round(robustness_score(0.73, 1.0, 0.10, 0.79, 0.13), digits=6))
