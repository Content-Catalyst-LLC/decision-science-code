# high_performance_sustainability_scan.jl

function robust_sustainability_score(value_score, average_performance, worst_case, pass_rate, performance_range)
    return 0.32 * value_score + 0.24 * average_performance + 0.22 * worst_case + 0.16 * pass_rate - 0.06 * performance_range
end

println("Robust sustainability score = ", round(robust_sustainability_score(0.72, 0.77, 0.68, 1.0, 0.14), digits=6))
