# expected_utility_surface_history.jl

function utility(x, risk_aversion)
    return 1.0 - exp(-risk_aversion * x)
end

probabilities = [0.42, 0.28, 0.18, 0.12]
payoffs = Dict(
    "Aggressive" => [128.0, 50.0, -90.0, -20.0],
    "Balanced" => [92.0, 68.0, 18.0, 42.0],
    "Defensive" => [62.0, 58.0, 44.0, 54.0],
    "Adaptive" => [88.0, 70.0, 36.0, 72.0]
)

for risk_aversion in [0.005, 0.01, 0.016, 0.03]
    println("risk aversion = ", risk_aversion)
    for (name, values) in payoffs
        eu = sum(probabilities .* [utility(v, risk_aversion) for v in values])
        println("  ", name, " EU = ", round(eu, digits=6))
    end
end
