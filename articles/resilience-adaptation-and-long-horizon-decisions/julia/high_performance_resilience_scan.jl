# high_performance_resilience_scan.jl

function resilient_decision_score(long_horizon_score, average_performance, worst_case, pass_rate, performance_range)
    return 0.30 * long_horizon_score + 0.24 * average_performance + 0.22 * worst_case + 0.18 * pass_rate - 0.06 * performance_range
end

println("Resilient decision score = ", round(resilient_decision_score(0.80, 0.79, 0.74, 1.0, 0.10), digits=6))
