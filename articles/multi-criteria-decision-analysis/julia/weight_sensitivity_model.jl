# weight_sensitivity_model.jl

function normalize_weights(values)
    return values ./ sum(values)
end

values = [0.16, 0.14, 0.16, 0.17, 0.13, 0.15, 0.09]
println("Weight sum = ", round(sum(normalize_weights(values)), digits=6))
