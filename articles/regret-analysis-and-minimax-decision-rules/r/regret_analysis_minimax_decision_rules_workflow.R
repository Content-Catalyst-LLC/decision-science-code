# regret_analysis_minimax_decision_rules_workflow.R
# Base R workflow for regret analysis and minimax decision rules:
# expected value, maximin, minimax regret, threshold compliance,
# vulnerability analysis, and decision-rule comparison.

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

payoffs <- read.csv(file.path(article_root, "data", "synthetic_payoff_matrix.csv"), stringsAsFactors = FALSE)
scenarios_data <- read.csv(file.path(article_root, "data", "synthetic_scenarios.csv"), stringsAsFactors = FALSE)
thresholds_data <- read.csv(file.path(article_root, "data", "synthetic_thresholds.csv"), stringsAsFactors = FALSE)

scenarios <- scenarios_data$scenario
scenario_weights <- setNames(scenarios_data$weight, scenarios_data$scenario)
thresholds <- setNames(thresholds_data$value, thresholds_data$threshold_name)

if (abs(sum(scenario_weights) - 1) > 1e-9) {
  stop("Scenario weights must sum to 1.")
}

performance_threshold <- thresholds["minimum_acceptable_performance"]
high_regret_threshold <- thresholds["high_regret_threshold"]
low_worst_case_threshold <- thresholds["low_worst_case_threshold"]
low_pass_rate_threshold <- thresholds["low_pass_rate_threshold"]

payoff_matrix <- as.matrix(payoffs[, scenarios])
scenario_bests <- apply(payoff_matrix, 2, max)

regret_matrix <- matrix(0, nrow = nrow(payoff_matrix), ncol = length(scenarios))
colnames(regret_matrix) <- scenarios

for (j in seq_along(scenarios)) {
  regret_matrix[, j] <- scenario_bests[j] - payoff_matrix[, j]
}

results <- data.frame(
  strategy = payoffs$strategy,
  expected_value = as.vector(payoff_matrix %*% scenario_weights[scenarios]),
  maximin_value = apply(payoff_matrix, 1, min),
  best_case = apply(payoff_matrix, 1, max),
  performance_range = apply(payoff_matrix, 1, max) - apply(payoff_matrix, 1, min),
  average_regret = rowMeans(regret_matrix),
  maximum_regret = apply(regret_matrix, 1, max),
  threshold_pass_rate = rowMeans(payoff_matrix >= performance_threshold),
  vulnerability_count = rowSums(payoff_matrix < performance_threshold),
  stringsAsFactors = FALSE
)

results$expected_value_rank <- rank(-results$expected_value, ties.method = "min")
results$maximin_rank <- rank(-results$maximin_value, ties.method = "min")
results$minimax_regret_rank <- rank(results$maximum_regret, ties.method = "min")
results$threshold_rank <- rank(-results$threshold_pass_rate, ties.method = "min")

results$combined_robustness_score <- (
  0.25 * results$maximin_value +
    0.25 * (1 - results$maximum_regret) +
    0.25 * results$threshold_pass_rate +
    0.15 * results$expected_value +
    0.10 * (1 - results$performance_range)
)

results$combined_rank <- rank(-results$combined_robustness_score, ties.method = "min")

results$review_flag <- ifelse(
  results$maximin_value < low_worst_case_threshold |
    results$maximum_regret > high_regret_threshold |
    results$threshold_pass_rate < low_pass_rate_threshold,
  "review",
  "acceptable"
)

results <- results[order(results$combined_rank), ]

write.csv(
  payoffs,
  file.path(tables_dir, "regret_payoff_matrix.csv"),
  row.names = FALSE
)

write.csv(
  data.frame(scenario = names(scenario_weights), weight = as.numeric(scenario_weights)),
  file.path(tables_dir, "regret_scenario_weights.csv"),
  row.names = FALSE
)

regret_table <- data.frame(
  strategy = payoffs$strategy,
  regret_matrix,
  check.names = FALSE,
  stringsAsFactors = FALSE
)

write.csv(
  regret_table,
  file.path(tables_dir, "regret_matrix.csv"),
  row.names = FALSE
)

vulnerability_table <- data.frame(
  strategy = payoffs$strategy,
  payoff_matrix < performance_threshold,
  check.names = FALSE,
  stringsAsFactors = FALSE
)

write.csv(
  vulnerability_table,
  file.path(tables_dir, "regret_vulnerability_table.csv"),
  row.names = FALSE
)

write.csv(
  results,
  file.path(tables_dir, "regret_decision_rule_comparison.csv"),
  row.names = FALSE
)

decision_rule_winners <- data.frame(
  rule = c("Expected value", "Maximin", "Minimax regret", "Threshold pass rate", "Combined robustness"),
  selected_strategy = c(
    results$strategy[which.min(results$expected_value_rank)],
    results$strategy[which.min(results$maximin_rank)],
    results$strategy[which.min(results$minimax_regret_rank)],
    results$strategy[which.min(results$threshold_rank)],
    results$strategy[which.min(results$combined_rank)]
  ),
  stringsAsFactors = FALSE
)

write.csv(
  decision_rule_winners,
  file.path(tables_dir, "regret_decision_rule_winners.csv"),
  row.names = FALSE
)

scenario_summary <- data.frame(
  scenario = scenarios,
  best_strategy = payoffs$strategy[apply(payoff_matrix, 2, which.max)],
  best_value = apply(payoff_matrix, 2, max),
  worst_strategy = payoffs$strategy[apply(payoff_matrix, 2, which.min)],
  worst_value = apply(payoff_matrix, 2, min),
  scenario_spread = apply(payoff_matrix, 2, max) - apply(payoff_matrix, 2, min),
  stringsAsFactors = FALSE
)

write.csv(
  scenario_summary,
  file.path(tables_dir, "regret_scenario_summary.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "maximum_regret_by_strategy.png"), width = 1200, height = 800)
barplot(
  results$maximum_regret,
  names.arg = results$strategy,
  las = 2,
  main = "Maximum Regret by Strategy",
  ylab = "Maximum regret"
)
grid()
dev.off()

png(file.path(figures_dir, "maximin_value_by_strategy.png"), width = 1200, height = 800)
barplot(
  results$maximin_value,
  names.arg = results$strategy,
  las = 2,
  main = "Maximin Value by Strategy",
  ylab = "Worst-case payoff"
)
grid()
dev.off()

png(file.path(figures_dir, "expected_value_vs_maximum_regret.png"), width = 1200, height = 800)
plot(
  results$expected_value,
  results$maximum_regret,
  xlab = "Expected value",
  ylab = "Maximum regret",
  main = "Expected Value vs Maximum Regret",
  pch = 19
)
text(
  results$expected_value,
  results$maximum_regret,
  labels = results$strategy,
  pos = 4,
  cex = 0.8
)
grid()
dev.off()

print(results)
print(regret_table)
print(decision_rule_winners)
print(scenario_summary)
