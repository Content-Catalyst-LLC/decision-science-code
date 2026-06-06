# high_performance_calibration_scan.jl

function brier_score(probability, outcome)
    return (probability - outcome)^2
end

function confidence_error(confidence, accuracy_proxy)
    return confidence - accuracy_proxy
end

println("Brier score = ", round(brier_score(0.69, 0.0), digits=6))
println("Confidence error = ", round(confidence_error(0.88, 0.52), digits=6))
