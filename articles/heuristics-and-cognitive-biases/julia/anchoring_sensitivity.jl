# anchoring_sensitivity.jl

function anchored_estimate(anchor, evidence, weight)
    return weight * anchor + (1 - weight) * evidence
end

for weight in [0.0, 0.25, 0.5, 0.75]
    println("weight=", weight, " estimate=", round(anchored_estimate(0.80, 0.42, weight), digits=6))
end
