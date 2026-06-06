# high_performance_strategy_scan.jl

function strategy_quality_score(expected_value, downside_robustness, dispersion, adaptability, capability_fit, governance_feasibility, reversibility)
    return 0.28 * expected_value / 100 + 0.22 * downside_robustness / 100 - 0.10 * dispersion / 30 + 0.14 * adaptability + 0.12 * capability_fit + 0.08 * governance_feasibility + 0.06 * reversibility
end

println("Strategy quality score = ", round(strategy_quality_score(76.7, 66.0, 9.2, 0.84, 0.72, 0.70, 0.82), digits=6))
