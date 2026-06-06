# decision_science_organizational_strategy_workflow.R
# Base R workflow for organizational strategy decision science:
# scenario comparison, robustness, adaptability, and review flags.

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
scenarios <- read.csv(file.path(article_root, "data", "synthetic_scenarios.csv"), stringsAsFactors = FALSE)
scenario_performance <- read.csv(file.path(article_root, "data", "synthetic_scenario_performance.csv"), stringsAsFactors = FALSE)

scenario_probs <- scenarios$probability
names(scenario_probs) <- scenarios$scenario

scenario_matrix <- strategies[, c("low_growth", "base_case", "high_growth", "disruption")]

strategies$expected_value <- (
  strategies$low_growth * scenario_probs["low_growth"] +
    strategies$base_case * scenario_probs["base_case"] +
    strategies$high_growth * scenario_probs["high_growth"] +
    strategies$disruption * scenario_probs["disruption"]
)

strategies$downside_robustness <- apply(scenario_matrix, 1, min)
strategies$scenario_dispersion <- apply(scenario_matrix, 1, sd)

strategies$strategy_quality_score <- (
  0.28 * strategies$expected_value / 100 +
    0.22 * strategies$downside_robustness / 100 -
    0.10 * strategies$scenario_dispersion / 30 +
    0.14 * strategies$adaptability +
    0.12 * strategies$capability_fit +
    0.08 * strategies$governance_feasibility +
    0.06 * strategies$reversibility
)

strategies$review_flag <- ifelse(
  strategies$downside_robustness < 50 |
    strategies$capability_fit < 0.55 |
    strategies$governance_feasibility < 0.55 |
    strategies$reversibility < 0.40,
  "review",
  "acceptable"
)

strategies$rank <- rank(-strategies$strategy_quality_score, ties.method = "min")
results <- strategies[order(strategies$rank), ]

write.csv(strategies, file.path(tables_dir, "organizational_strategy_profiles.csv"), row.names = FALSE)
write.csv(scenario_performance, file.path(tables_dir, "organizational_strategy_scenario_performance.csv"), row.names = FALSE)
write.csv(results, file.path(tables_dir, "organizational_strategy_decision_profiles.csv"), row.names = FALSE)

png(file.path(figures_dir, "organizational_strategy_quality_scores.png"), width = 1200, height = 800)
barplot(
  results$strategy_quality_score,
  names.arg = results$strategy,
  las = 2,
  main = "Strategic Option Quality Scores",
  ylab = "Decision quality score"
)
grid()
dev.off()

png(file.path(figures_dir, "organizational_strategy_downside_robustness.png"), width = 1200, height = 800)
barplot(
  results$downside_robustness,
  names.arg = results$strategy,
  las = 2,
  main = "Downside Robustness by Strategic Option",
  ylab = "Worst scenario outcome"
)
grid()
dev.off()

print(results)
