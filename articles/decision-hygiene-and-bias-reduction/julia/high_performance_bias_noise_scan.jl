# high_performance_bias_noise_scan.jl

function bias(errors)
    return sum(errors) / length(errors)
end

function mse(errors)
    return sum(e -> e^2, errors) / length(errors)
end

errors = [0.12, 0.04, -0.03, 0.08]
println("Bias = ", round(bias(errors), digits=6))
println("MSE = ", round(mse(errors), digits=6))
