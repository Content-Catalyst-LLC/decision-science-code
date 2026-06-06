# calibration_frontier.jl

function brier_score(probability, outcome)
    return (probability - outcome)^2
end

for p in [0.1, 0.3, 0.5, 0.7, 0.9]
    println("p=", p, " brier_if_event=", round(brier_score(p, 1.0), digits=6))
end
