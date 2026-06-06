# collective_error_frontier.jl

function collective_error(group_estimate, true_value)
    return abs(group_estimate - true_value)
end

for pair in [(0.64, 0.62), (0.70, 0.56), (0.52, 0.69)]
    println("Collective error = ", round(collective_error(pair[1], pair[2]), digits=6))
end
