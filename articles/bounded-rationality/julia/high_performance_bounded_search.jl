# high_performance_bounded_search.jl

function first_satisficing(values, aspiration)
    for (idx, value) in enumerate(values)
        if value >= aspiration
            return idx, value
        end
    end
    return argmax(values), maximum(values)
end

values = [0.58, 0.71, 0.82, 0.77, 0.91]
idx, value = first_satisficing(values, 0.75)
println("Satisficing option = ", idx, " value = ", value)
println("Optimizing option = ", argmax(values), " value = ", maximum(values))
