# infrastructure_value_model.jl

function expected_value(values, probabilities)
    total = 0.0
    for i in eachindex(values)
        total += values[i] * probabilities[i]
    end
    return total
end

values = [76.0, 76.0, 82.0, 70.0, 78.0]
probabilities = [0.30, 0.20, 0.20, 0.15, 0.15]
println("Expected service value = ", round(expected_value(values, probabilities), digits=6))
println("Worst-case value = ", minimum(values))
