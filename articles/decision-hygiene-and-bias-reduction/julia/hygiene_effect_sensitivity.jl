# hygiene_effect_sensitivity.jl

function post_hygiene_error(pre_error, hygiene_effect)
    return pre_error * (1 - hygiene_effect)
end

for effect in [0.15, 0.30, 0.55]
    println("Post-hygiene error = ", round(post_hygiene_error(0.20, effect), digits=6))
end
