# implementation_drift_model.jl

function drift_next(current_drift, feedback_quality, implementation_capacity, random_component)
    return max(0.0, current_drift + random_component - 0.030 * feedback_quality - 0.020 * implementation_capacity)
end

println("Implementation drift next = ", round(drift_next(6.0, 12.0, 22.0, 0.40), digits=6))
