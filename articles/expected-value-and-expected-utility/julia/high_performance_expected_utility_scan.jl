# high_performance_expected_utility_scan.jl

prospects = Dict(
    "Safe Option" => [(100.0, 1.0)],
    "Balanced Gamble" => [(180.0, 0.60), (40.0, 0.40)],
    "High-Risk Gamble" => [(400.0, 0.25), (0.0, 0.75)],
    "Catastrophic Downside" => [(260.0, 0.45), (-120.0, 0.55)],
    "Resilient Moderate Upside" => [(150.0, 0.70), (70.0, 0.30)]
)

function ev(pairs)
    sum(x * p for (x, p) in pairs)
end

function crra(x, rho; offset=151.0)
    z = x + offset
    if abs(rho - 1.0) < 1e-8
        return log(z)
    end
    return (z^(1.0-rho) - 1.0) / (1.0-rho)
end

function eu(pairs, rho)
    sum(p * crra(x, rho) for (x, p) in pairs)
end

for (name, pairs) in prospects
    println(name, " EV=", round(ev(pairs), digits=4), " EU(rho=1)=", round(eu(pairs, 1.0), digits=6))
end
