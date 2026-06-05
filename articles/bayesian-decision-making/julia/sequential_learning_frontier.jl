# sequential_learning_frontier.jl

function update_positive(prior, sensitivity, false_positive_rate)
    return (sensitivity * prior) / (sensitivity * prior + false_positive_rate * (1.0 - prior))
end

function update_negative(prior, sensitivity, false_positive_rate)
    return ((1.0 - sensitivity) * prior) / (((1.0 - sensitivity) * prior) + ((1.0 - false_positive_rate) * (1.0 - prior)))
end

posterior = 0.10
signals = ["positive", "positive", "negative", "positive"]

for signal in signals
    if signal == "positive"
        posterior = update_positive(posterior, 0.86, 0.12)
    else
        posterior = update_negative(posterior, 0.86, 0.12)
    end
    println(signal, " posterior=", round(posterior, digits=6))
end
