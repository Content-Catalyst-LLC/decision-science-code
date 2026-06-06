# regret_frontier.jl

function regret(score, best_score)
    return best_score - score
end

println("Regret = ", round(regret(0.72, 0.91), digits=6))
