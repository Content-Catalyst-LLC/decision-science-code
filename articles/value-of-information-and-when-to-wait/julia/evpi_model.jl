# evpi_model.jl

function evpi(perfect_information_value, current_expected_value)
    return perfect_information_value - current_expected_value
end

println("EVPI = ", round(evpi(76.4, 68.1), digits=6))
