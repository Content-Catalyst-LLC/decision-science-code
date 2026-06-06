# strategy_vector_similarity.jl

function cosine_similarity(a, b)
    return sum(a .* b) / (sqrt(sum(a .^ 2)) * sqrt(sum(b .^ 2)))
end

a = [0.68, 0.88, 0.82, 0.93, 0.86]
s = [0.20, 0.25, 0.18, 0.22, 0.15]
println("Cosine alignment = ", round(cosine_similarity(a, s), digits=6))
