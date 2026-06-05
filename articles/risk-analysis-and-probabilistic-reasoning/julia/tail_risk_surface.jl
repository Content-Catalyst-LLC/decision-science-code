# tail_risk_surface.jl

function tail_penalty(expected_loss, volatility, cvar, breach_probability)
    return expected_loss * 0.35 + volatility * 0.20 + abs(cvar) * 0.30 + breach_probability * 0.15
end

println("Conservative penalty = ", round(tail_penalty(0.002, 0.027, -0.020, 0.001), digits=6))
println("High-risk penalty = ", round(tail_penalty(0.045, 0.190, -0.380, 0.180), digits=6))
