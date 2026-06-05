# certainty_equivalent_frontier.jl

function inverse_crra(u, rho; offset=151.0)
    if abs(rho - 1.0) < 1e-8
        return exp(u) - offset
    end
    return (u * (1.0-rho) + 1.0)^(1.0/(1.0-rho)) - offset
end

for rho in [0.25, 1.0, 2.25]
    println("rho=", rho, " example CE=", round(inverse_crra(5.2, rho), digits=4))
end
