# path_dependence_lock_in_decision_timing_workflow.R
# Base R workflow for path dependence, lock-in, and decision timing:
# strategy comparison, switching costs, lock-in risk,
# timing sensitivity, scenario performance, and generated outputs.

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

paths <- read.csv(file.path(article_root, "data", "synthetic_path_profiles.csv"), stringsAsFactors = FALSE)
scenario_performance <- read.csv(file.path(article_root, "data", "synthetic_scenario_performance.csv"), stringsAsFactors = FALSE)

paths$path_quality_score <- (
  0.24 * paths$initial_value +
    0.24 * paths$future_flexibility -
    0.16 * paths$switching_cost -
    0.18 * paths$lock_in_risk +
    0.14 * paths$reversibility -
    0.04 * paths$timing_sensitivity
)

paths$review_flag <- ifelse(
  paths$switching_cost > 0.65 |
    paths$lock_in_risk > 0.70 |
    paths$reversibility < 0.35,
  "review",
  "acceptable"
)

scenario_split <- split(scenario_performance$performance, scenario_performance$path)

scenario_summary <- data.frame(
  path = names(scenario_split),
  average_scenario_performance = as.numeric(sapply(scenario_split, mean)),
  worst_case_performance = as.numeric(sapply(scenario_split, min)),
  performance_range = as.numeric(sapply(scenario_split, function(x) max(x) - min(x))),
  threshold_pass_rate = as.numeric(sapply(scenario_split, function(x) mean(x >= 0.70))),
  stringsAsFactors = FALSE
)

results <- merge(paths, scenario_summary, by = "path")

results$timing_adjusted_score <- (
  0.30 * results$path_quality_score +
    0.24 * results$average_scenario_performance +
    0.22 * results$worst_case_performance +
    0.18 * results$threshold_pass_rate -
    0.06 * results$performance_range
)

results$review_flag <- ifelse(
  results$review_flag == "review" |
    results$worst_case_performance < 0.55 |
    results$threshold_pass_rate < 0.60,
  "review",
  "acceptable"
)

results$rank <- rank(-results$timing_adjusted_score, ties.method = "min")
results <- results[order(results$rank), ]

write.csv(paths, file.path(tables_dir, "path_dependence_profiles.csv"), row.names = FALSE)
write.csv(scenario_performance, file.path(tables_dir, "path_dependence_scenario_performance.csv"), row.names = FALSE)
write.csv(scenario_summary, file.path(tables_dir, "path_dependence_scenario_summary.csv"), row.names = FALSE)
write.csv(results, file.path(tables_dir, "path_dependence_decision_results.csv"), row.names = FALSE)

png(file.path(figures_dir, "path_dependence_timing_adjusted_scores.png"), width = 1200, height = 800)
barplot(
  results$timing_adjusted_score,
  names.arg = results$path,
  las = 2,
  main = "Timing-Adjusted Path Decision Score",
  ylab = "Score"
)
grid()
dev.off()

png(file.path(figures_dir, "lock_in_risk_by_path.png"), width = 1200, height = 800)
barplot(
  results$lock_in_risk,
  names.arg = results$path,
  las = 2,
  main = "Lock-In Risk by Path",
  ylab = "Lock-in risk"
)
grid()
dev.off()

print(results)
