# high_performance_voi_scan.jl

function expected_value(values, probabilities)
    return sum(values .* probabilities)
end

values = [82.0, 28.0, 40.0, 76.0]
probabilities = [0.35, 0.25, 0.20, 0.20]
println("Expected value = ", round(expected_value(values, probabilities), digits=6))
