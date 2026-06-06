# feedback_state_model.jl

function feedback_update(state, reinforcing, balancing, disturbance)
    return state + reinforcing - balancing + disturbance
end

println("Next state = ", round(feedback_update(52.0, 3.0, 1.4, -0.2), digits=6))
