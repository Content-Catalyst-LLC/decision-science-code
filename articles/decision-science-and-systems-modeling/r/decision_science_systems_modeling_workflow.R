# decision_science_systems_modeling_workflow.R
# Base R workflow for decision science and systems modeling:
# intervention comparison, delay sensitivity, resilience,
# scenario performance, threshold review, and generated outputs.

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

strategies$dynamic_intervention_score <- (
  0.22 * strategies$stability_score +
    0.18 * strategies$responsiveness_score -
    0.20 * strategies$delay_sensitivity +
    0.26 * strategies$resilience_score +
    0.14 * strategies$transparency_score
)

strategies$review_flag <- ifelse(
  strategies$delay_sensitivity > 0.70 |
    strategies$resilience_score < 0.60 |
    strategies$transparency_score < 0.55,
  "review",
  "acceptable"
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

results$systems_decision_score <- (
  0.35 * results$dynamic_intervention_score +
    0.25 * results$average_scenario_performance +
    0.20 * results$worst_case_performance +
    0.20 * results$threshold_pass_rate
)

results$systems_decision_rank <- rank(-results$systems_decision_score, ties.method = "min")
results$review_flag <- ifelse(
  results$review_flag == "review" | results$worst_case_performance < 0.60,
  "review",
  "acceptable"
)
results <- results[order(results$systems_decision_rank), ]

write.csv(
  strategies,
  file.path(tables_dir, "systems_modeling_strategy_profiles.csv"),
  row.names = FALSE
)

write.csv(
  scenario_performance,
  file.path(tables_dir, "systems_modeling_scenario_performance.csv"),
  row.names = FALSE
)

write.csv(
  scenario_summary,
  file.path(tables_dir, "systems_modeling_scenario_summary.csv"),
  row.names = FALSE
)

write.csv(
  results,
  file.path(tables_dir, "systems_modeling_decision_results.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "systems_modeling_strategy_scores.png"), width = 1200, height = 800)
barplot(
  results$systems_decision_score,
  names.arg = results$strategy,
  las = 2,
  main = "Systems Decision Score by Strategy",
  ylab = "Score"
)
grid()
dev.off()

png(file.path(figures_dir, "systems_modeling_worst_case_performance.png"), width = 1200, height = 800)
barplot(
  results$worst_case_performance,
  names.arg = results$strategy,
  las = 2,
  main = "Worst-Case Scenario Performance",
  ylab = "Worst-case performance"
)
grid()
dev.off()

print(results)
