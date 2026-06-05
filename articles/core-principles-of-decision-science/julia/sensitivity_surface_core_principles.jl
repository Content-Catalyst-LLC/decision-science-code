# sensitivity_surface_core_principles.jl

base_score = 0.86
for delta in -0.10:0.05:0.10
    revised_score = base_score + delta * 0.45
    println("delta=", delta, " revised score=", round(revised_score, digits=4))
end
