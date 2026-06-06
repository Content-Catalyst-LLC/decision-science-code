# high_performance_governance_scan.jl

function governance_score(quality, legitimacy, accountability, implementation, traceability, review, monitoring, corrective, risk, burden)
    return 0.16 * quality + 0.14 * legitimacy + 0.16 * accountability + 0.12 * implementation + 0.10 * traceability + 0.10 * review + 0.10 * monitoring + 0.10 * corrective - 0.08 * risk - 0.04 * burden
end

println("Governance score = ", round(governance_score(0.86, 0.84, 0.90, 0.84, 0.86, 0.88, 0.90, 0.92, 0.30, 0.68), digits=6))
