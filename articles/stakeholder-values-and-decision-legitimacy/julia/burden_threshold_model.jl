# burden_threshold_model.jl

function burden_review(max_burden, threshold)
    return max_burden > threshold
end

println("Review required = ", burden_review(0.62, 0.50))
