# robust_decision_making_workflow.R
# Base R workflow for robust decision-making.

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
set.seed(42)

strategies <- read.csv(file.path(article_root, "data", "synthetic_strategies.csv"), stringsAsFactors = FALSE)
scenario_data <- read.csv(file.path(article_root, "data", "synthetic_scenarios.csv"), stringsAsFactors = FALSE)
performance <- read.csv(file.path(article_root, "data", "synthetic_performance_matrix.csv"), stringsAsFactors = FALSE)
thresholds_data <- read.csv(file.path(article_root, "data", "synthetic_thresholds.csv"), stringsAsFactors = FALSE)

scenarios <- scenario_data$scenario
scenario_weights <- setNames(scenario_data$weight, scenario_data$scenario)
thresholds <- setNames(thresholds_data$value, thresholds_data$threshold_name)
if (abs(sum(scenario_weights) - 1) > 1e-9) stop("Scenario weights must sum to 1.")

performance_threshold <- thresholds["minimum_acceptable_performance"]
performance_matrix <- as.matrix(performance[, scenarios])
scenario_maxima <- apply(performance_matrix, 2, max)
regret_matrix <- matrix(0, nrow = nrow(performance_matrix), ncol = length(scenarios))
colnames(regret_matrix) <- scenarios
for (j in seq_along(scenarios)) {
  regret_matrix[, j] <- scenario_maxima[j] - performance_matrix[, j]
}

results <- data.frame(
  strategy = performance$strategy,
  expected_value = as.vector(performance_matrix %*% scenario_weights),
  worst_case = apply(performance_matrix, 1, min),
  best_case = apply(performance_matrix, 1, max),
  performance_range = apply(performance_matrix, 1, max) - apply(performance_matrix, 1, min),
  average_regret = rowMeans(regret_matrix),
  max_regret = apply(regret_matrix, 1, max),
  threshold_pass_rate = rowMeans(performance_matrix >= performance_threshold),
  vulnerability_count = rowSums(performance_matrix < performance_threshold),
  stringsAsFactors = FALSE
)

results$robustness_score <- (
  0.30 * results$worst_case +
    0.25 * results$threshold_pass_rate +
    0.20 * (1 - results$max_regret) +
    0.15 * results$expected_value +
    0.10 * (1 - results$performance_range)
)
results$rank <- rank(-results$robustness_score, ties.method = "min")
results$review_flag <- ifelse(
  results$worst_case < thresholds["low_worst_case_threshold"] |
    results$max_regret > thresholds["high_regret_threshold"] |
    results$threshold_pass_rate < thresholds["low_pass_rate_threshold"],
  "review",
  "acceptable"
)
results <- results[order(results$rank), ]

write.csv(performance, file.path(tables_dir, "rdm_strategy_performance_matrix.csv"), row.names = FALSE)
write.csv(data.frame(scenario = names(scenario_weights), weight = as.numeric(scenario_weights)), file.path(tables_dir, "rdm_scenario_weights.csv"), row.names = FALSE)
write.csv(results, file.path(tables_dir, "rdm_robustness_results.csv"), row.names = FALSE)
write.csv(data.frame(strategy = performance$strategy, regret_matrix, check.names = FALSE), file.path(tables_dir, "rdm_regret_matrix.csv"), row.names = FALSE)
write.csv(data.frame(strategy = performance$strategy, performance_matrix < performance_threshold, check.names = FALSE), file.path(tables_dir, "rdm_vulnerability_table.csv"), row.names = FALSE)

scenario_summary <- data.frame(
  scenario = scenarios,
  best_strategy = performance$strategy[apply(performance_matrix, 2, which.max)],
  max_performance = apply(performance_matrix, 2, max),
  min_performance = apply(performance_matrix, 2, min),
  scenario_spread = apply(performance_matrix, 2, max) - apply(performance_matrix, 2, min),
  stringsAsFactors = FALSE
)
write.csv(scenario_summary, file.path(tables_dir, "rdm_scenario_summary.csv"), row.names = FALSE)

simulation_records <- list()
summary_records <- list()
record_counter <- 1
for (i in seq_len(nrow(strategies))) {
  value <- 100
  values <- numeric(40)
  growth_rates <- numeric(40)
  for (t in seq_len(40)) {
    regime_shift <- sample(c(-2.8, -1.2, 0.0, 1.0, 2.1), size = 1, prob = c(0.10, 0.20, 0.30, 0.25, 0.15))
    shock <- rnorm(1, mean = 0, sd = strategies$volatility[i])
    adaptive_buffer <- strategies$adaptability[i] * runif(1, 0.4, 1.3)
    resilience_buffer <- strategies$resilience[i] * runif(1, 0.3, 1.0)
    growth <- strategies$base_return[i] + regime_shift + shock + adaptive_buffer + resilience_buffer
    value <- max(20, value * (1 + growth / 100))
    values[t] <- value
    growth_rates[t] <- growth
    simulation_records[[record_counter]] <- data.frame(strategy = strategies$strategy[i], time = t, strategy_value_index = value, growth_rate = growth, regime_shift = regime_shift, shock = shock, stringsAsFactors = FALSE)
    record_counter <- record_counter + 1
  }
  summary_records[[i]] <- data.frame(strategy = strategies$strategy[i], final_value = values[length(values)], min_value = min(values), max_value = max(values), average_value = mean(values), value_volatility = sd(values), average_growth_rate = mean(growth_rates), worst_growth_rate = min(growth_rates), stringsAsFactors = FALSE)
}

simulation_table <- do.call(rbind, simulation_records)
simulation_summary <- do.call(rbind, summary_records)
simulation_summary <- simulation_summary[order(-simulation_summary$final_value), ]
write.csv(simulation_table, file.path(tables_dir, "rdm_strategy_durability_simulation.csv"), row.names = FALSE)
write.csv(simulation_summary, file.path(tables_dir, "rdm_strategy_durability_summary.csv"), row.names = FALSE)

png(file.path(figures_dir, "rdm_robustness_scores.png"), width = 1200, height = 800)
barplot(results$robustness_score, names.arg = results$strategy, las = 2, main = "Robustness Scores Across Strategies", ylab = "Robustness score")
grid()
dev.off()

png(file.path(figures_dir, "rdm_worst_case_performance.png"), width = 1200, height = 800)
barplot(results$worst_case, names.arg = results$strategy, las = 2, main = "Worst-Case Strategy Performance", ylab = "Worst-case performance")
grid()
dev.off()

png(file.path(figures_dir, "rdm_max_regret.png"), width = 1200, height = 800)
barplot(results$max_regret, names.arg = results$strategy, las = 2, main = "Maximum Regret by Strategy", ylab = "Maximum regret")
grid()
dev.off()

print(results)
print(scenario_summary)
print(simulation_summary)
