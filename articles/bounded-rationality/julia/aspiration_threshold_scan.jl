# aspiration_threshold_scan.jl

function update_aspiration(current, feedback, eta)
    return clamp(current + eta * (feedback - current), 0.35, 0.95)
end

asp = 0.70
for feedback in [0.74, 0.68, 0.76]
    global asp = update_aspiration(asp, feedback, 0.12)
    println(round(asp, digits=6))
end
