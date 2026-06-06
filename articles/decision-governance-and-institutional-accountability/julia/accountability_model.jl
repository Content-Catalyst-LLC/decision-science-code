# accountability_model.jl

function accountability_score(decision_rights, evidence_traceability, review_strength, ownership, monitoring, corrective_capacity)
    return 0.18 * decision_rights + 0.17 * evidence_traceability + 0.18 * review_strength + 0.17 * ownership + 0.15 * monitoring + 0.15 * corrective_capacity
end

println("Accountability score = ", round(accountability_score(0.82, 0.86, 0.88, 0.84, 0.90, 0.92), digits=6))
