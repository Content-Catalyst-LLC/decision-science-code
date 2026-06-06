# high_performance_bayesian_update.jl

function posterior_from_likelihoods(prior, likelihood_true, likelihood_false)
    odds = prior / (1 - prior)
    posterior_odds = odds * (likelihood_true / likelihood_false)
    return posterior_odds / (1 + posterior_odds)
end

println("Posterior = ", round(posterior_from_likelihoods(0.35, 0.72, 0.28), digits=6))
