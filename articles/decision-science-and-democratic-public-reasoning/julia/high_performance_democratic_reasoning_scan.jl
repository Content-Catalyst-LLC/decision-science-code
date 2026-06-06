# high_performance_democratic_reasoning_scan.jl

function democratic_decision_quality(evidence, transparency, participation, fairness, contestability, equity, accountability, uncertainty, burden, trust_risk)
    return 0.14 * evidence + 0.12 * transparency + 0.14 * participation + 0.14 * fairness + 0.12 * contestability + 0.12 * equity + 0.12 * accountability + 0.10 * uncertainty - 0.05 * burden - 0.10 * trust_risk
end

println("Democratic decision quality = ", round(democratic_decision_quality(0.84, 0.88, 0.88, 0.88, 0.86, 0.86, 0.88, 0.86, 0.76, 0.28), digits=6))
