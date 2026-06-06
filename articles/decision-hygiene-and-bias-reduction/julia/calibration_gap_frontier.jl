# calibration_gap_frontier.jl

function calibration_gap(predicted, observed)
    return predicted - observed
end

for pair in [(0.75, 0.62), (0.55, 0.47), (0.85, 0.70)]
    println("Calibration gap = ", round(calibration_gap(pair[1], pair[2]), digits=6))
end
