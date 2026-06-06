# switching_cost_model.jl

function switching_cost(investment, network_dependence, institutional_routine)
    return 0.36 * investment + 0.34 * network_dependence + 0.30 * institutional_routine
end

println("Switching cost = ", round(switching_cost(0.55, 0.62, 0.58), digits=6))
