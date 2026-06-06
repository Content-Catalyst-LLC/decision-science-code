# high_performance_policy_scan.jl

function robust_policy_score(policy_value_score, average_performance, worst_case, pass_rate, performance_range)
    return 0.32 * policy_value_score + 0.24 * average_performance + 0.22 * worst_case + 0.16 * pass_rate - 0.06 * performance_range
end

println("Robust public policy score = ", round(robust_policy_score(0.76, 0.77, 0.72, 1.0, 0.10), digits=6))
