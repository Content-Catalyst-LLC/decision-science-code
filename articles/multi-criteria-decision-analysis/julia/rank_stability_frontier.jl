# rank_stability_frontier.jl

function best_rank_rate(ranks)
    return count(rank -> rank == 1, ranks) / length(ranks)
end

ranks = [1, 1, 2, 3, 1, 2]
println("Best-rank rate = ", round(best_rank_rate(ranks), digits=6))
