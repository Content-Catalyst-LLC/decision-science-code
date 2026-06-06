# robustness_model.jl

function worst_case(values)
    return minimum(values)
end

function threshold_pass_rate(values, threshold)
    return count(x -> x >= threshold, values) / length(values)
end

values = [0.78, 0.76, 0.82, 0.80, 0.81]
println("Worst case = ", round(worst_case(values), digits=6))
println("Threshold pass rate = ", round(threshold_pass_rate(values, 0.70), digits=6))
