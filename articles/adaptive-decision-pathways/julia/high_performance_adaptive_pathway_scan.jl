# high_performance_adaptive_pathway_scan.jl

function robust_adaptive_score(adaptive_pathway_score, average_performance, worst_case, pass_rate, performance_range)
    return 0.30 * adaptive_pathway_score + 0.24 * average_performance + 0.22 * worst_case + 0.18 * pass_rate - 0.06 * performance_range
end

println("Robust adaptive score = ", round(robust_adaptive_score(0.78, 0.79, 0.74, 1.0, 0.10), digits=6))
