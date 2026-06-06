# resilience_adaptation_long_horizon_workflow.R
# Base R workflow for resilience, adaptation, and long-horizon decisions:
# strategy comparison, scenario performance, threshold review,
# and generated outputs.

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

strategies <- read.csv(file.path(article_root, "data", "synthetic_strategy_profiles.csv"), stringsAsFactors = FALSE)
scenario_performance <- read.csv(file.path(article_root, "data", "synthetic_scenario_performance.csv"), stringsAsFactors = FALSE)

strategies$long_horizon_score <- (
  0.24 * strategies$resilience_score +
    0.22 * strategies$adaptability_score -
    0.12 * strategies$near_term_cost +
    0.24 * strategies$long_term_value +
    0.18 * strategies$reversibility
)

scenario_split <- split(scenario_performance$performance, scenario_performance$strategy)

scenario_summary <- data.frame(
  strategy = names(scenario_split),
  average_scenario_performance = as.numeric(sapply(scenario_split, mean)),
  worst_case_performance = as.numeric(sapply(scenario_split, min)),
  performance_range = as.numeric(sapply(scenario_split, function(x) max(x) - min(x))),
  threshold_pass_rate = as.numeric(sapply(scenario_split, function(x) mean(x >= 0.70))),
  stringsAsFactors = FALSE
)

results <- merge(strategies, scenario_summary, by = "strategy")

results$resilient_decision_score <- (
  0.30 * results$long_horizon_score +
    0.24 * results$average_scenario_performance +
    0.22 * results$worst_case_performance +
    0.18 * results$threshold_pass_rate -
    0.06 * results$performance_range
)

results$review_flag <- ifelse(
  results$worst_case_performance < 0.60 |
    results$threshold_pass_rate < 0.60 |
    results$resilience_score < 0.50 |
    results$adaptability_score < 0.50,
  "review",
  "acceptable"
)

results$rank <- rank(-results$resilient_decision_score, ties.method = "min")
results <- results[order(results$rank), ]

write.csv(
  strategies,
  file.path(tables_dir, "long_horizon_strategy_profiles.csv"),
  row.names = FALSE
)

write.csv(
  scenario_performance,
  file.path(tables_dir, "long_horizon_scenario_performance.csv"),
  row.names = FALSE
)

write.csv(
  scenario_summary,
  file.path(tables_dir, "long_horizon_scenario_summary.csv"),
  row.names = FALSE
)

write.csv(
  results,
  file.path(tables_dir, "resilience_adaptation_decision_results.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "resilient_decision_scores.png"), width = 1200, height = 800)
barplot(
  results$resilient_decision_score,
  names.arg = results$strategy,
  las = 2,
  main = "Resilient Long-Horizon Decision Score",
  ylab = "Score"
)
grid()
dev.off()

png(file.path(figures_dir, "long_horizon_worst_case_performance.png"), width = 1200, height = 800)
barplot(
  results$worst_case_performance,
  names.arg = results$strategy,
  las = 2,
  main = "Worst-Case Long-Horizon Scenario Performance",
  ylab = "Worst-case performance"
)
grid()
dev.off()

print(results)
