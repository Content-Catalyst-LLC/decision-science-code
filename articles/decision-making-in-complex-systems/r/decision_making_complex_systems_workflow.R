# decision_making_complex_systems_workflow.R
# Base R workflow for decision-making in complex systems:
# strategy profiles, scenario performance, threshold review,
# adaptive robustness, and generated figures.

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

strategies$complex_system_score <- (
  0.18 * strategies$adaptability +
    0.18 * strategies$robustness +
    0.16 * strategies$feedback_awareness +
    0.16 * strategies$interdependence_handling -
    0.10 * strategies$coordination_burden +
    0.12 * strategies$legitimacy +
    0.20 * strategies$threshold_resilience
)

strategies$vulnerability_flag <- ifelse(
  strategies$robustness < 0.60 |
    strategies$feedback_awareness < 0.55 |
    strategies$threshold_resilience < 0.60 |
    strategies$coordination_burden > 0.70,
  "review",
  "acceptable"
)

strategies$rank <- rank(-strategies$complex_system_score, ties.method = "min")
strategies <- strategies[order(strategies$rank), ]

scenario_summary <- aggregate(
  performance ~ strategy,
  data = scenario_performance,
  FUN = function(x) paste(
    round(mean(x), 6),
    round(min(x), 6),
    round(max(x) - min(x), 6),
    round(mean(x >= 0.70), 6),
    sep = "|"
  )
)

parsed <- do.call(rbind, strsplit(as.character(scenario_summary$performance), "\\|"))
scenario_summary <- data.frame(
  strategy = scenario_summary$strategy,
  average_scenario_performance = as.numeric(parsed[, 1]),
  worst_case_performance = as.numeric(parsed[, 2]),
  performance_range = as.numeric(parsed[, 3]),
  threshold_pass_rate = as.numeric(parsed[, 4]),
  stringsAsFactors = FALSE
)

combined <- merge(strategies, scenario_summary, by = "strategy")

combined$adaptive_robustness_score <- (
  0.35 * combined$complex_system_score +
    0.25 * combined$average_scenario_performance +
    0.20 * combined$worst_case_performance +
    0.20 * combined$threshold_pass_rate
)

combined$adaptive_robustness_rank <- rank(-combined$adaptive_robustness_score, ties.method = "min")
combined$review_flag <- ifelse(
  combined$vulnerability_flag == "review" | combined$worst_case_performance < 0.60,
  "review",
  "acceptable"
)
combined <- combined[order(combined$adaptive_robustness_rank), ]

write.csv(
  strategies,
  file.path(tables_dir, "complex_system_strategy_profiles.csv"),
  row.names = FALSE
)

write.csv(
  scenario_performance,
  file.path(tables_dir, "complex_system_scenario_performance.csv"),
  row.names = FALSE
)

write.csv(
  scenario_summary,
  file.path(tables_dir, "complex_system_scenario_summary.csv"),
  row.names = FALSE
)

write.csv(
  combined,
  file.path(tables_dir, "complex_system_decision_results.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "complex_system_strategy_scores.png"), width = 1200, height = 800)
barplot(
  combined$adaptive_robustness_score,
  names.arg = combined$strategy,
  las = 2,
  main = "Adaptive Robustness Score by Strategy",
  ylab = "Score"
)
grid()
dev.off()

png(file.path(figures_dir, "complex_system_worst_case_performance.png"), width = 1200, height = 800)
barplot(
  combined$worst_case_performance,
  names.arg = combined$strategy,
  las = 2,
  main = "Worst-Case Scenario Performance",
  ylab = "Worst-case performance"
)
grid()
dev.off()

print(combined)
