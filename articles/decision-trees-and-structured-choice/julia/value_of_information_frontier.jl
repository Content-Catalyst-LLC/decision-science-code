# value_of_information_frontier.jl

immediate_ev = 125.0 * 0.58 + -35.0 * 0.42
staged_ev = 145.0 * 0.54 + -20.0 * 0.46 - 12.0 + 18.0

println("Immediate EV = ", round(immediate_ev, digits=4))
println("Staged EV = ", round(staged_ev, digits=4))
println("Net information value = ", round(staged_ev - immediate_ev, digits=4))
