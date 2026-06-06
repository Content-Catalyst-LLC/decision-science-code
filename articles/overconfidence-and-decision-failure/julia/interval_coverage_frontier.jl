# interval_coverage_frontier.jl

function interval_hit(lower, upper, actual)
    return lower <= actual <= upper
end

hits = [interval_hit(90, 150, 154), interval_hit(70, 110, 96), interval_hit(35, 55, 58)]
coverage = sum(hits) / length(hits)
println("Coverage = ", round(coverage, digits=6))
