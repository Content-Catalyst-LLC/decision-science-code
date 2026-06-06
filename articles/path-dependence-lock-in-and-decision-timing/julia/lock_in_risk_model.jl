# lock_in_risk_model.jl

function lock_in_risk(switching_cost, institutional_routine, network_dependence, option_value)
    return 0.42 * switching_cost + 0.28 * institutional_routine + 0.20 * network_dependence - 0.10 * option_value
end

println("Lock-in risk = ", round(lock_in_risk(0.58, 0.62, 0.55, 0.40), digits=6))
