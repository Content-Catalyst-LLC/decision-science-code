# trigger_point_model.jl

function trigger_hit(system_stress, option_value, stress_trigger, option_value_trigger)
    return system_stress >= stress_trigger || option_value <= option_value_trigger
end

println("Trigger hit? ", trigger_hit(0.70, 0.55, 0.68, 0.40))
