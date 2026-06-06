function legitimacy(transparency, participation, contestability, accountability)
    return 0.26 * transparency + 0.24 * participation + 0.25 * contestability + 0.25 * accountability
end
println("Legitimacy = ", round(legitimacy(0.82, 0.80, 0.86, 0.90), digits=6))
