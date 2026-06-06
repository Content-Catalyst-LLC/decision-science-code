# legitimacy_model.jl

function legitimacy_score(transparency, participation, procedural_fairness, evidence_quality, contestability, accountability)
    return 0.17 * transparency + 0.17 * participation + 0.18 * procedural_fairness + 0.16 * evidence_quality + 0.16 * contestability + 0.16 * accountability
end

println("Legitimacy score = ", round(legitimacy_score(0.88, 0.88, 0.88, 0.84, 0.86, 0.88), digits=6))
