# decision_trees_structured_choice_workflow.R
# Base R workflow for rolling back a multi-stage decision tree,
# testing sensitivity, and estimating value of information.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)

if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}

setwd(article_root)

tables_dir <- file.path(article_root, "outputs", "tables")
figures_dir <- file.path(article_root, "outputs", "figures")
dir.create(tables_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(figures_dir, recursive = TRUE, showWarnings = FALSE)

strategies <- read.csv(file.path(article_root, "data", "synthetic_tree_strategies.csv"), stringsAsFactors = FALSE)

strategies$failure_probability <- 1 - strategies$success_probability

strategies$expected_value <- (
  strategies$success_payoff * strategies$success_probability +
  strategies$failure_payoff * strategies$failure_probability -
  strategies$information_cost +
  strategies$flexibility_credit
)

strategies$minimum_outcome <- pmin(strategies$success_payoff, strategies$failure_payoff)
strategies$maximum_outcome <- pmax(strategies$success_payoff, strategies$failure_payoff)
strategies$outcome_spread <- strategies$maximum_outcome - strategies$minimum_outcome

strategies$robust_score <- (
  0.60 * strategies$expected_value +
  0.25 * strategies$minimum_outcome -
  0.15 * strategies$outcome_spread
)

strategies$expected_value_rank <- rank(-strategies$expected_value, ties.method = "min")
strategies$robust_rank <- rank(-strategies$robust_score, ties.method = "min")
strategies <- strategies[order(-strategies$expected_value), ]

write.csv(strategies, file.path(tables_dir, "decision_tree_rollback_profiles.csv"), row.names = FALSE)

immediate_ev <- strategies$expected_value[strategies$strategy == "Immediate Action"]
staged_ev <- strategies$expected_value[strategies$strategy == "Staged Learning"]

value_of_information <- data.frame(
  comparison = "Staged Learning vs Immediate Action",
  immediate_expected_value = immediate_ev,
  staged_expected_value = staged_ev,
  net_value_of_information = staged_ev - immediate_ev,
  stringsAsFactors = FALSE
)

write.csv(value_of_information, file.path(tables_dir, "value_of_information_summary.csv"), row.names = FALSE)

probability_grid <- seq(0.30, 0.85, by = 0.01)
sensitivity_rows <- data.frame()

for (strategy_name in strategies$strategy) {
  base_row <- strategies[strategies$strategy == strategy_name, ]

  for (p in probability_grid) {
    ev <- (
      base_row$success_payoff * p +
      base_row$failure_payoff * (1 - p) -
      base_row$information_cost +
      base_row$flexibility_credit
    )

    sensitivity_rows <- rbind(
      sensitivity_rows,
      data.frame(
        strategy = strategy_name,
        success_probability = p,
        expected_value = ev,
        stringsAsFactors = FALSE
      )
    )
  }
}

write.csv(sensitivity_rows, file.path(tables_dir, "decision_tree_probability_sensitivity.csv"), row.names = FALSE)

baseline_value <- strategies$expected_value[strategies$strategy == "Conservative Baseline"]
threshold_rows <- data.frame()

for (strategy_name in unique(sensitivity_rows$strategy)) {
  subset_rows <- sensitivity_rows[sensitivity_rows$strategy == strategy_name, ]
  feasible <- subset_rows[subset_rows$expected_value >= baseline_value, ]

  threshold_probability <- if (nrow(feasible) == 0) {
    NA
  } else {
    min(feasible$success_probability)
  }

  threshold_rows <- rbind(
    threshold_rows,
    data.frame(
      strategy = strategy_name,
      threshold_to_exceed_baseline = threshold_probability,
      baseline_expected_value = baseline_value,
      stringsAsFactors = FALSE
    )
  )
}

write.csv(threshold_rows, file.path(tables_dir, "decision_tree_threshold_analysis.csv"), row.names = FALSE)

regret_rows <- data.frame()

states <- c("success", "failure")

for (state in states) {
  if (state == "success") {
    state_values <- strategies$success_payoff - strategies$information_cost + strategies$flexibility_credit
  } else {
    state_values <- strategies$failure_payoff - strategies$information_cost + strategies$flexibility_credit
  }

  best_value <- max(state_values)

  regret_rows <- rbind(
    regret_rows,
    data.frame(
      strategy = strategies$strategy,
      state = state,
      realized_value = state_values,
      best_state_value = best_value,
      regret = best_value - state_values,
      stringsAsFactors = FALSE
    )
  )
}

write.csv(regret_rows, file.path(tables_dir, "decision_tree_regret_summary.csv"), row.names = FALSE)

png(file.path(figures_dir, "expected_value_by_strategy.png"), width = 1200, height = 800)
barplot(
  strategies$expected_value,
  names.arg = strategies$strategy,
  las = 2,
  main = "Expected Value by Decision-Tree Strategy",
  ylab = "Expected value"
)
grid()
dev.off()

png(file.path(figures_dir, "robust_score_by_strategy.png"), width = 1200, height = 800)
barplot(
  strategies$robust_score,
  names.arg = strategies$strategy,
  las = 2,
  main = "Robust Score by Decision-Tree Strategy",
  ylab = "Robust score"
)
grid()
dev.off()

png(file.path(figures_dir, "probability_sensitivity_curves.png"), width = 1200, height = 800)
plot(
  sensitivity_rows$success_probability,
  sensitivity_rows$expected_value,
  type = "n",
  xlab = "Success probability",
  ylab = "Expected value",
  main = "Decision-Tree Probability Sensitivity"
)

for (strategy_name in unique(sensitivity_rows$strategy)) {
  subset_rows <- sensitivity_rows[sensitivity_rows$strategy == strategy_name, ]
  lines(subset_rows$success_probability, subset_rows$expected_value, type = "l")
}

legend("topleft", legend = unique(sensitivity_rows$strategy), bty = "n", cex = 0.85)
grid()
dev.off()

print(strategies)
print(value_of_information)
print(threshold_rows)
