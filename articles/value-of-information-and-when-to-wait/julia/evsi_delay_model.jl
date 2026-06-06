# evsi_delay_model.jl

function net_value_waiting(evsi, information_cost, delay_cost)
    return evsi - information_cost - delay_cost
end

println("Net value waiting = ", round(net_value_waiting(4.4, 2.0, 1.3), digits=6))
