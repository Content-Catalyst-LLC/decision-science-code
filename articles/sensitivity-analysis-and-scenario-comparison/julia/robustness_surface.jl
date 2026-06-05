# robustness_surface.jl

function robustness_score(average, minimum, worst, max_regret, volatility)
    return 0.35 * average + 0.30 * minimum + 0.20 * worst - 0.10 * max_regret - 0.05 * volatility
end

println("Balanced robustness = ", round(robustness_score(75.0, 62.0, 50.0, 14.0, 8.0), digits=4))
println("Adaptive robustness = ", round(robustness_score(77.0, 65.0, 53.0, 11.0, 7.0), digits=4))
