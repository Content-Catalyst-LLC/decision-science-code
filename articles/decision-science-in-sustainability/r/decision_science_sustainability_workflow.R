# decision_science_sustainability_workflow.R
# Base R workflow for decision science in sustainability:
# strategy scoring, scenario robustness, threshold review,
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

strategies$sustainability_value_score <- (
  0.22 * strategies$emissions_reduction +
    0.20 * strategies$social_equity -
    0.12 * strategies$cost_burden +
    0.18 * strategies$resilience_score +
    0.12 * strategies$implementation_feasibility +
    0.16 * strategies$threshold_protection
)

strategies$review_flag <- ifelse(
  strategies$social_equity < 0.50 |
    strategies$resilience_score < 0.50 |
    strategies$threshold_protection < 0.55 |
    strategies$cost_burden > 0.70,
  "review",
  "acceptable"
)

scenario_split <- split(scenario_performance$performance, scenario_performance$strategy)

scenario_summary <- data.frame(
  strategy = names(scenario_split),
  average_performance = as.numeric(sapply(scenario_split, mean)),
  worst_case_performance = as.numeric(sapply(scenario_split, min)),
  performance_range = as.numeric(sapply(scenario_split, function(x) max(x) - min(x))),
  threshold_pass_rate = as.numeric(sapply(scenario_split, function(x) mean(x >= 0.65))),
  stringsAsFactors = FALSE
)

results <- merge(strategies, scenario_summary, by = "strategy")

results$robust_sustainability_score <- (
  0.32 * results$sustainability_value_score +
    0.24 * results$average_performance +
    0.22 * results$worst_case_performance +
    0.16 * results$threshold_pass_rate -
    0.06 * results$performance_range
)

results$review_flag <- ifelse(
  results$review_flag == "review" |
    results$worst_case_performance < 0.50 |
    results$threshold_pass_rate < 0.60,
  "review",
  "acceptable"
)

results$rank <- rank(-results$robust_sustainability_score, ties.method = "min")
results <- results[order(results$rank), ]

write.csv(strategies, file.path(tables_dir, "sustainability_strategy_profiles.csv"), row.names = FALSE)
write.csv(scenario_performance, file.path(tables_dir, "sustainability_scenario_performance.csv"), row.names = FALSE)
write.csv(scenario_summary, file.path(tables_dir, "sustainability_scenario_summary.csv"), row.names = FALSE)
write.csv(results, file.path(tables_dir, "sustainability_decision_results.csv"), row.names = FALSE)

png(file.path(figures_dir, "sustainability_robust_scores.png"), width = 1200, height = 800)
barplot(
  results$robust_sustainability_score,
  names.arg = results$strategy,
  las = 2,
  main = "Robust Sustainability Strategy Score",
  ylab = "Score"
)
grid()
dev.off()

png(file.path(figures_dir, "sustainability_worst_case_performance.png"), width = 1200, height = 800)
barplot(
  results$worst_case_performance,
  names.arg = results$strategy,
  las = 2,
  main = "Worst-Case Sustainability Strategy Performance",
  ylab = "Worst-case performance"
)
grid()
dev.off()

print(results)
