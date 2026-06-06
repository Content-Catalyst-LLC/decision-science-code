# policy_resistance_model.jl

function net_policy_effect(policy_delta, intended_strength, resistance_strength, resistance_response)
    return intended_strength * policy_delta - resistance_strength * resistance_response
end

println("Net policy effect = ", round(net_policy_effect(10.0, 0.8, 0.4, 6.0), digits=6))
