# high_performance_forecast_evaluation.jl

function brier_score(probability, outcome)
    return (probability - outcome)^2
end

function log_loss(probability, outcome)
    p = clamp(probability, 0.01, 0.99)
    return -(outcome * log(p) + (1 - outcome) * log(1 - p))
end

probabilities = [0.62, 0.74, 0.41, 0.57, 0.68]
outcomes = [1, 1, 0, 1, 0]

println("Mean Brier score = ", round(sum(brier_score.(probabilities, outcomes)) / length(probabilities), digits=6))
println("Mean log loss = ", round(sum(log_loss.(probabilities, outcomes)) / length(probabilities), digits=6))
