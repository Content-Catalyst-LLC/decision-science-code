# stakeholder_score_model.jl

function stakeholder_score(values, weights)
    return sum(values .* weights)
end

println("Score = ", round(stakeholder_score([0.76, 0.82, 0.74], [0.2, 0.4, 0.4]), digits=6))
