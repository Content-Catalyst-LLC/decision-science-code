# feedback_sensitivity_model.jl

function feedback_update(state, reinforcing, balancing, disturbance)
    return state + reinforcing - balancing + disturbance
end

println("Next state = ", round(feedback_update(55.0, 3.85, 2.10, -0.4), digits=6))
