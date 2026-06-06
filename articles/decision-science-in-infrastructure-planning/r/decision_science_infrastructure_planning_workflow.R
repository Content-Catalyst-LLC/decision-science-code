# decision_science_infrastructure_planning_workflow.R
# Base R workflow for infrastructure planning decision science:
# scenario comparison, lifecycle value, robustness, equity, and review flags.

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

alternatives <- read.csv(file.path(article_root, "data", "synthetic_infrastructure_alternatives.csv"), stringsAsFactors = FALSE)
scenarios <- read.csv(file.path(article_root, "data", "synthetic_scenarios.csv"), stringsAsFactors = FALSE)
scenario_performance <- read.csv(file.path(article_root, "data", "synthetic_scenario_performance.csv"), stringsAsFactors = FALSE)

scenario_probs <- scenarios$probability
names(scenario_probs) <- scenarios$scenario

scenario_matrix <- alternatives[, c("baseline", "climate_stress", "demand_growth", "funding_constraint", "disruption")]

alternatives$expected_service_value <- (
  alternatives$baseline * scenario_probs["baseline"] +
    alternatives$climate_stress * scenario_probs["climate_stress"] +
    alternatives$demand_growth * scenario_probs["demand_growth"] +
    alternatives$funding_constraint * scenario_probs["funding_constraint"] +
    alternatives$disruption * scenario_probs["disruption"]
)

alternatives$worst_case_value <- apply(scenario_matrix, 1, min)
alternatives$scenario_dispersion <- apply(scenario_matrix, 1, sd)

alternatives$infrastructure_decision_score <- (
  0.22 * alternatives$expected_service_value / 100 +
    0.20 * alternatives$worst_case_value / 100 -
    0.10 * alternatives$scenario_dispersion / 30 -
    0.12 * alternatives$lifecycle_cost +
    0.14 * alternatives$equity_score +
    0.14 * alternatives$resilience_score +
    0.10 * alternatives$environmental_score +
    0.06 * alternatives$implementation_feasibility +
    0.06 * alternatives$adaptability
)

alternatives$review_flag <- ifelse(
  alternatives$worst_case_value < 50 |
    alternatives$equity_score < 0.55 |
    alternatives$resilience_score < 0.55 |
    alternatives$environmental_score < 0.50 |
    alternatives$implementation_feasibility < 0.50,
  "review",
  "acceptable"
)

alternatives$rank <- rank(-alternatives$infrastructure_decision_score, ties.method = "min")
results <- alternatives[order(alternatives$rank), ]

write.csv(alternatives, file.path(tables_dir, "infrastructure_alternative_profiles.csv"), row.names = FALSE)
write.csv(scenario_performance, file.path(tables_dir, "infrastructure_scenario_performance.csv"), row.names = FALSE)
write.csv(results, file.path(tables_dir, "infrastructure_decision_results.csv"), row.names = FALSE)

png(file.path(figures_dir, "infrastructure_decision_scores.png"), width = 1200, height = 800)
barplot(
  results$infrastructure_decision_score,
  names.arg = results$alternative,
  las = 2,
  main = "Infrastructure Decision Scores",
  ylab = "Decision score"
)
grid()
dev.off()

png(file.path(figures_dir, "infrastructure_worst_case_value.png"), width = 1200, height = 800)
barplot(
  results$worst_case_value,
  names.arg = results$alternative,
  las = 2,
  main = "Worst-Case Infrastructure Value",
  ylab = "Worst-case scenario value"
)
grid()
dev.off()

print(results)
