# future_maturity_model.jl

function future_maturity_score(ai, governance, uncertainty, legitimacy, reproducibility, systems, ethics, adaptive, failure)
    return max(0.0, min(1.0, 0.12 * ai + 0.14 * governance + 0.14 * uncertainty + 0.12 * legitimacy + 0.12 * reproducibility + 0.12 * systems + 0.14 * ethics + 0.14 * adaptive - 0.14 * failure))
end

println("Future maturity = ", round(future_maturity_score(0.86, 0.90, 0.88, 0.84, 0.88, 0.86, 0.90, 0.88, 0.24), digits=6))
