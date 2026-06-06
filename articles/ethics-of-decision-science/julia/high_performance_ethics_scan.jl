function net_ethical_score(expected_value, equity, safety, legitimacy, transparency, contestability, reversibility, accountability, harm, opacity, exclusion)
    ethical_value = 0.18 * expected_value / 100 + 0.18 * equity + 0.16 * safety + 0.14 * legitimacy + 0.10 * transparency + 0.10 * contestability + 0.08 * reversibility + 0.06 * accountability
    ethical_risk = 0.34 * harm + 0.22 * opacity + 0.24 * exclusion + 0.20 * (1.0 - accountability)
    return ethical_value - 0.42 * ethical_risk
end
println("Net ethical score = ", round(net_ethical_score(82, 0.84, 0.82, 0.84, 0.82, 0.86, 0.88, 0.90, 0.30, 0.28, 0.24), digits=6))
