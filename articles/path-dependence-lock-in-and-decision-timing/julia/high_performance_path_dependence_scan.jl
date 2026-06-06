# high_performance_path_dependence_scan.jl

function timing_adjusted_score(path_quality, average_performance, worst_case, pass_rate, performance_range)
    return 0.30 * path_quality + 0.24 * average_performance + 0.22 * worst_case + 0.18 * pass_rate - 0.06 * performance_range
end

println("Timing-adjusted score = ", round(timing_adjusted_score(0.60, 0.79, 0.74, 1.0, 0.10), digits=6))
