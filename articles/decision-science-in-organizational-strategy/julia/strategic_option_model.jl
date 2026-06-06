# strategic_option_model.jl

function expected_value(values, probabilities)
    total = 0.0
    for i in eachindex(values)
        total += values[i] * probabilities[i]
    end
    return total
end

values = [68.0, 82.0, 89.0, 66.0]
probabilities = [0.25, 0.35, 0.20, 0.20]
println("Expected value = ", round(expected_value(values, probabilities), digits=6))
println("Downside robustness = ", minimum(values))
