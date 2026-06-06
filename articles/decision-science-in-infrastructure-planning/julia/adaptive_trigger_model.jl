# adaptive_trigger_model.jl

function trigger_reached(indicator, threshold)
    return indicator >= threshold
end

println("Adaptive trigger reached = ", trigger_reached(0.74, 0.70))
