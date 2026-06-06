# high_performance_influence_scan.jl

function normalize_weights(values)
    total = sum(values)
    return values ./ total
end

function influence_concentration(weights)
    return maximum(weights)
end

weights = normalize_weights([0.72, 0.61, 0.80, 0.47, 0.69, 0.58, 0.84])
println("Influence concentration = ", round(influence_concentration(weights), digits=6))
