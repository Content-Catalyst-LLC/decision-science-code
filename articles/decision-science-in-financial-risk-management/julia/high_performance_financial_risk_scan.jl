# high_performance_financial_risk_scan.jl

function risk_resilience_score(expected_loss, worst_case, dispersion, liquidity, governance, model_confidence)
    return 0.24 * liquidity + 0.22 * governance + 0.18 * model_confidence - 0.16 * abs(expected_loss) / 30 - 0.14 * abs(worst_case) / 30 - 0.06 * dispersion / 10
end

println("Risk resilience score = ", round(risk_resilience_score(-4.2, -9.4, 3.1, 0.76, 0.84, 0.78), digits=6))
