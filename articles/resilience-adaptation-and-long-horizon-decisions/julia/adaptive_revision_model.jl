# adaptive_revision_model.jl

function should_revise(system_state, resilience_capacity, stress_threshold, resilience_threshold)
    return system_state >= stress_threshold || resilience_capacity <= resilience_threshold
end

println("Revise? ", should_revise(72.0, 24.0, 80.0, 25.0))
