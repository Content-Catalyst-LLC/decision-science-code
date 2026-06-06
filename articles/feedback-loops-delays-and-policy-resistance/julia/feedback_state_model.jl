# feedback_state_model.jl

function feedback_update(state, reinforcing, balancing, resistance, disturbance)
    return state + reinforcing - balancing + resistance + disturbance
end

println("Next state = ", round(feedback_update(50.0, 4.0, 1.12, 0.4, -0.3), digits=6))
