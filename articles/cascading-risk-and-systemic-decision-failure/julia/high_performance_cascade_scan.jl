# high_performance_cascade_scan.jl

function resilience_adjusted_score(average_continuity, worst_case, pass_rate, cascade_risk, continuity_range)
    return 0.30 * average_continuity + 0.25 * worst_case + 0.20 * pass_rate - 0.15 * cascade_risk - 0.10 * continuity_range
end

println("Resilience-adjusted score = ", round(resilience_adjusted_score(0.79, 0.74, 1.0, 0.32, 0.10), digits=6))
