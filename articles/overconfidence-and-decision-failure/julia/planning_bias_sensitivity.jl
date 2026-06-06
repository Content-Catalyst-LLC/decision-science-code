# planning_bias_sensitivity.jl

function planning_error(actual, estimate)
    return (actual - estimate) / estimate
end

for pair in [(154.0, 120.0), (520.0, 365.0), (48.0, 30.0)]
    println("Planning error = ", round(planning_error(pair[1], pair[2]), digits=6))
end
