# high_performance_deep_uncertainty_scan.jl

function robustness_score(worst_case, pass_rate, max_regret, expected_value, performance_range)
    return 0.28 * worst_case + 0.24 * pass_rate + 0.20 * (1 - max_regret) + 0.18 * expected_value + 0.10 * (1 - performance_range)
end

println("Deep uncertainty robustness score = ", round(robustness_score(0.72, 1.0, 0.12, 0.78, 0.15), digits=6))
