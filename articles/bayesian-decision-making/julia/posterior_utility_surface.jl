# posterior_utility_surface.jl

function posterior_expected_utility(posterior, utility_true, utility_false)
    return posterior * utility_true + (1.0 - posterior) * utility_false
end

for posterior in [0.10, 0.25, 0.50, 0.75]
    action_utility = posterior_expected_utility(posterior, 90.0, -25.0)
    wait_utility = posterior_expected_utility(posterior, -80.0, 15.0)
    println("posterior=", posterior, " action utility=", round(action_utility, digits=4), " wait utility=", round(wait_utility, digits=4))
end
