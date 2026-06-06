# high_performance_infrastructure_scan.jl

function infrastructure_decision_score(expected_value, worst_case, dispersion, lifecycle_cost, equity, resilience, environmental, feasibility, adaptability)
    return 0.22 * expected_value / 100 + 0.20 * worst_case / 100 - 0.10 * dispersion / 30 - 0.12 * lifecycle_cost + 0.14 * equity + 0.14 * resilience + 0.10 * environmental + 0.06 * feasibility + 0.06 * adaptability
end

println("Infrastructure decision score = ", round(infrastructure_decision_score(77.1, 70.0, 4.1, 0.66, 0.74, 0.84, 0.76, 0.66, 0.90), digits=6))
