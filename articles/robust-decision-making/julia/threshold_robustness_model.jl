function threshold_pass_rate(values, threshold)
    return count(x -> x >= threshold, values) / length(values)
end
println("Pass rate = ", round(threshold_pass_rate([0.73, 0.77, 0.79, 0.81], 0.70), digits=6))
