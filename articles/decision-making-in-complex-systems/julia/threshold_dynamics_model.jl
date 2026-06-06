# threshold_dynamics_model.jl

function threshold_breach_rate(values, threshold)
    return count(x -> x >= threshold, values) / length(values)
end

println("Threshold breach rate = ", round(threshold_breach_rate([55, 61, 72, 68, 74], 70), digits=6))
