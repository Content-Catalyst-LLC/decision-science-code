# queue_pressure_model.jl

function queue_next(current_queue, arrivals, discharges)
    return max(0.0, current_queue + arrivals - discharges)
end

function queue_pressure(queue, reference_capacity)
    return min(1.0, queue / reference_capacity)
end

q = queue_next(18.0, 24.0, 22.0)
println("Queue next = ", round(q, digits=6))
println("Queue pressure = ", round(queue_pressure(q, 60.0), digits=6))
