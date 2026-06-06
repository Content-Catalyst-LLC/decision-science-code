# alignment_drift_model.jl

function drift(alignment)
    return 1.0 - alignment
end

println("Strategic drift = ", round(drift(0.91), digits=6))
