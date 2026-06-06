# high_performance_ai_governance_scan.jl

function ai_governance_score(expected_value, worst_case, dispersion, evidence, oversight, equity, transparency, security, feasibility)
    return 0.20 * expected_value / 100 + 0.18 * worst_case / 100 - 0.08 * dispersion / 30 + 0.14 * evidence + 0.14 * oversight + 0.12 * equity + 0.10 * transparency + 0.08 * security + 0.06 * feasibility
end

println("AI governance score = ", round(ai_governance_score(78.0, 76.0, 2.2, 0.76, 0.82, 0.80, 0.78, 0.82, 0.72), digits=6))
