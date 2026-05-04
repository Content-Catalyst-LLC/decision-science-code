# Decision Science: Multi-Criteria Decision Analysis in R
# Educational example only.

library(tidyverse)

alternatives <- read_csv("../data/decision_alternatives.csv", show_col_types = FALSE)

weights <- tibble(
  criterion = c(
    "cost_efficiency",
    "effectiveness",
    "equity",
    "feasibility",
    "resilience",
    "implementation_risk"
  ),
  weight = c(0.16, 0.22, 0.18, 0.16, 0.20, -0.08)
)

alternatives_long <- alternatives |>
  pivot_longer(
    cols = -alternative,
    names_to = "criterion",
    values_to = "value"
  ) |>
  left_join(weights, by = "criterion") |>
  mutate(weighted_value = value * weight)

scores <- alternatives_long |>
  group_by(alternative) |>
  summarise(
    decision_score = sum(weighted_value),
    .groups = "drop"
  ) |>
  arrange(desc(decision_score))

tradeoff_flags <- alternatives |>
  mutate(
    high_implementation_risk = implementation_risk > 0.55,
    low_equity = equity < 0.60,
    low_resilience = resilience < 0.60,
    requires_deliberation =
      high_implementation_risk | low_equity | low_resilience
  )

dir.create("../outputs", showWarnings = FALSE, recursive = TRUE)

write_csv(alternatives, "../outputs/r_decision_alternatives.csv")
write_csv(alternatives_long, "../outputs/r_decision_alternatives_long.csv")
write_csv(scores, "../outputs/r_mcda_scores.csv")
write_csv(tradeoff_flags, "../outputs/r_decision_tradeoff_flags.csv")

print(scores)
print(tradeoff_flags)
