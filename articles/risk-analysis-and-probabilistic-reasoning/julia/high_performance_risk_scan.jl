# high_performance_risk_scan.jl

strategies = Dict(
    "Conservative Strategy" => (0.035, 0.025, 0.010, -0.045, 0.010),
    "Balanced Strategy" => (0.065, 0.070, 0.025, -0.100, 0.015),
    "High-Risk Strategy" => (0.105, 0.165, 0.055, -0.260, 0.000),
    "Adaptive Strategy" => (0.075, 0.090, 0.030, -0.140, 0.030),
    "Resilient Strategy" => (0.060, 0.050, 0.015, -0.070, 0.045)
)

function expected_stress_return(mean_return, shock_probability, shock_size, recovery_credit)
    return mean_return + shock_probability * shock_size + recovery_credit
end

for (name, values) in strategies
    mean_return, volatility, shock_probability, shock_size, recovery_credit = values
    println(name, " expected stress baseline = ", round(expected_stress_return(mean_return, shock_probability, shock_size, recovery_credit), digits=6))
end
