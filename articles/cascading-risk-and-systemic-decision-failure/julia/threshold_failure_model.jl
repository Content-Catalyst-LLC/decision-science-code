# threshold_failure_model.jl

function threshold_failure(stress, neighbor_failure_load, buffer, threshold)
    effective_stress = stress + neighbor_failure_load + max(0.0, 0.40 - buffer)
    return effective_stress >= threshold
end

println("Threshold failure? ", threshold_failure(0.52, 0.18, 0.31, 0.66))
