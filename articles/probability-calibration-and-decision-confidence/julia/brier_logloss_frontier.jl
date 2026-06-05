# brier_logloss_frontier.jl

function brier_score(probability, outcome)
    return (probability - outcome)^2
end

for probability in [0.1, 0.3, 0.5, 0.7, 0.9]
    println("p=", probability, " Brier if event occurs=", round(brier_score(probability, 1), digits=4))
end
