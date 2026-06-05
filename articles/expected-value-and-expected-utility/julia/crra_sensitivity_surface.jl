# crra_sensitivity_surface.jl

function crra(x, rho; offset=151.0)
    z = x + offset
    if abs(rho - 1.0) < 1e-8
        return log(z)
    end
    return (z^(1.0-rho) - 1.0) / (1.0-rho)
end

prospect = [(180.0, 0.60), (40.0, 0.40)]
for rho in [0.25, 0.75, 1.0, 1.5, 2.25]
    eu = sum(p * crra(x, rho) for (x, p) in prospect)
    println("rho=", rho, " expected utility=", round(eu, digits=6))
end
