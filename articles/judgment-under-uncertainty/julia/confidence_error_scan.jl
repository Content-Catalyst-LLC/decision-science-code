# confidence_error_scan.jl

function confidence_gap(confidence, forecast_probability)
    return confidence - forecast_probability
end

for pair in [(0.72, 0.62), (0.60, 0.70), (0.81, 0.78)]
    println("gap=", round(confidence_gap(pair[1], pair[2]), digits=6))
end
