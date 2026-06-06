# high_performance_healthcare_scan.jl

function robust_healthcare_score(value_score, average_performance, worst_case, pass_rate, performance_range)
    return 0.34 * value_score + 0.24 * average_performance + 0.22 * worst_case + 0.14 * pass_rate - 0.06 * performance_range
end

println("Robust healthcare score = ", round(robust_healthcare_score(0.62, 0.74, 0.68, 1.0, 0.16), digits=6))
