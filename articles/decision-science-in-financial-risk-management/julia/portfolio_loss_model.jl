# portfolio_loss_model.jl

function expected_loss(losses, probabilities)
    total = 0.0
    for i in eachindex(losses)
        total += losses[i] * probabilities[i]
    end
    return total
end

losses = [-1.2, -4.8, -3.6, -6.2]
probs = [0.55, 0.20, 0.15, 0.10]
println("Expected loss = ", round(expected_loss(losses, probs), digits=6))
println("Worst case = ", minimum(losses))
