# expected_utility_surface.jl

function utility(x, risk_aversion)
    return 1.0 - exp(-risk_aversion * x)
end

probabilities = [0.22, 0.34, 0.18, 0.16, 0.10]
payoffs = Dict(
    "Optimize" => [145.0, 92.0, 30.0, -95.0, -40.0],
    "Balanced" => [112.0, 84.0, 58.0, 12.0, 30.0],
    "Robust" => [78.0, 72.0, 65.0, 48.0, 55.0]
)

for risk_aversion in [0.005, 0.01, 0.018, 0.03]
    println("risk aversion = ", risk_aversion)
    for (name, values) in payoffs
        eu = sum(probabilities .* [utility(v, risk_aversion) for v in values])
        println("  ", name, " EU = ", round(eu, digits=6))
    end
end
