# high_performance_scenario_scan.jl

function scenario_robustness_score(expected_value, worst_case, threshold_pass_rate, maximum_regret, dispersion)
    return 0.26 * expected_value + 0.24 * worst_case + 0.20 * threshold_pass_rate - 0.16 * maximum_regret - 0.14 * dispersion
end

println("Scenario robustness score = ", round(scenario_robustness_score(0.78, 0.76, 1.0, 0.10, 0.03), digits=6))
