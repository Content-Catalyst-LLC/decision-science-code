# outcome_bias_monte_carlo.jl

using Random
Random.seed!(42)

function simulate_outcomes(expected_value, downside_exposure, learning, accountability, safeguards, trials)
    favorable = 0
    for _ in 1:trials
        shock = randn() * 22.0
        implementation_noise = randn() * 8.0
        adverse_exposure = max(0.0, 0.45 + 0.30 * randn())
        outcome = expected_value - 45.0 * downside_exposure * adverse_exposure + 18.0 * learning + 14.0 * accountability + 10.0 * safeguards + shock + implementation_noise
        if outcome >= 75.0
            favorable += 1
        end
    end
    return favorable / trials
end

println("Fast Commitment favorable rate = ", round(simulate_outcomes(88, 0.72, 0.28, 0.34, 0.30, 1000), digits=4))
println("Staged Learning favorable rate = ", round(simulate_outcomes(74, 0.18, 0.96, 0.94, 0.86, 1000), digits=4))
