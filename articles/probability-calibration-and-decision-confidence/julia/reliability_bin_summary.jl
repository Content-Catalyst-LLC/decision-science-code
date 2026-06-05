# reliability_bin_summary.jl

function calibration_gap(probabilities, outcomes)
    return sum(probabilities) / length(probabilities) - sum(outcomes) / length(outcomes)
end

println("Calibration gap = ", round(calibration_gap([0.72, 0.76, 0.79], [1, 1, 0]), digits=6))
