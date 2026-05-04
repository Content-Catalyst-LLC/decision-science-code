# Decision Science: Regret and Robustness in R
# Educational example only.

library(tidyverse)

scenario_values <- read_csv("../data/scenario_values.csv", show_col_types = FALSE)

robustness <- scenario_values |>
  group_by(alternative) |>
  summarise(
    worst_case_value = min(value),
    mean_value = mean(value),
    best_case_value = max(value),
    .groups = "drop"
  )

regret <- scenario_values |>
  group_by(scenario) |>
  mutate(best_value_in_scenario = max(value)) |>
  ungroup() |>
  mutate(regret = best_value_in_scenario - value)

max_regret <- regret |>
  group_by(alternative) |>
  summarise(
    maximum_regret = max(regret),
    .groups = "drop"
  ) |>
  arrange(maximum_regret)

dir.create("../outputs", showWarnings = FALSE, recursive = TRUE)

write_csv(robustness, "../outputs/r_robustness_summary.csv")
write_csv(regret, "../outputs/r_regret_table.csv")
write_csv(max_regret, "../outputs/r_max_regret.csv")

print(robustness)
print(max_regret)
