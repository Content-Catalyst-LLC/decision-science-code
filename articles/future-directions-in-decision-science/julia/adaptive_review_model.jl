# adaptive_review_model.jl

function review_required(governance, uncertainty, ethics, adaptive, failure)
    return governance <= 0.58 || uncertainty <= 0.58 || ethics <= 0.58 || adaptive <= 0.58 || failure >= 0.62
end

println("Review required = ", review_required(0.54, 0.62, 0.50, 0.54, 0.56))
