# high_performance_complex_system_scan.jl

function complex_system_score(adaptability, robustness, feedback, interdependence, burden, legitimacy, threshold_resilience)
    return 0.18 * adaptability + 0.18 * robustness + 0.16 * feedback + 0.16 * interdependence - 0.10 * burden + 0.12 * legitimacy + 0.20 * threshold_resilience
end

println("Complex-system score = ", round(complex_system_score(0.81, 0.86, 0.82, 0.83, 0.44, 0.78, 0.86), digits=6))
