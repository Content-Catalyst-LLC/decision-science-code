# priority_sensitivity_model.jl

function normalize_weights(values)
    return values ./ sum(values)
end

values = [0.18, 0.18, 0.20, 0.18, 0.14, 0.12]
println("Weight sum = ", round(sum(normalize_weights(values)), digits=6))
