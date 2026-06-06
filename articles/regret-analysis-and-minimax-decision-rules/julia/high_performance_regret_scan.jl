# high_performance_regret_scan.jl

function regret(value, scenario_best)
    return scenario_best - value
end

println("Regret = ", round(regret(0.72, 0.91), digits=6))
