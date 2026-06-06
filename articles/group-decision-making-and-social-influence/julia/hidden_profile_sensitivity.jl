# hidden_profile_sensitivity.jl

function hidden_profile_risk(shared_information, unique_information)
    return unique_information / (shared_information + unique_information)
end

for pair in [(8, 5), (5, 9), (4, 10)]
    println("Hidden-profile risk = ", round(hidden_profile_risk(pair[1], pair[2]), digits=6))
end
