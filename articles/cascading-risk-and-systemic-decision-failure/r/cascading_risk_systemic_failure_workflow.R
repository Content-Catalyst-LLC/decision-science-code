# cascading_risk_systemic_failure_workflow.R
# Base R workflow for cascading risk and systemic decision failure:
# vulnerability scoring, scenario performance, threshold review,
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

systems <- read.csv(file.path(article_root, "data", "synthetic_system_profiles.csv"), stringsAsFactors = FALSE)
scenario_performance <- read.csv(file.path(article_root, "data", "synthetic_scenario_performance.csv"), stringsAsFactors = FALSE)

systems$cascade_risk_score <- (
  0.22 * systems$exposure +
    0.22 * systems$dependency_centrality +
    0.20 * systems$buffer_weakness +
    0.18 * systems$common_mode_risk -
    0.09 * systems$monitoring_quality -
    0.09 * systems$response_capacity
)

systems$review_flag <- ifelse(
  systems$cascade_risk_score > 0.55 |
    systems$buffer_weakness > 0.70 |
    systems$common_mode_risk > 0.70 |
    systems$response_capacity < 0.45,
  "review",
  "acceptable"
)

scenario_split <- split(scenario_performance$service_continuity, scenario_performance$system)

scenario_summary <- data.frame(
  system = names(scenario_split),
  average_continuity = as.numeric(sapply(scenario_split, mean)),
  worst_case_continuity = as.numeric(sapply(scenario_split, min)),
  continuity_range = as.numeric(sapply(scenario_split, function(x) max(x) - min(x))),
  threshold_pass_rate = as.numeric(sapply(scenario_split, function(x) mean(x >= 0.70))),
  stringsAsFactors = FALSE
)

results <- merge(systems, scenario_summary, by = "system")

results$resilience_adjusted_score <- (
  0.30 * results$average_continuity +
    0.25 * results$worst_case_continuity +
    0.20 * results$threshold_pass_rate -
    0.15 * results$cascade_risk_score -
    0.10 * results$continuity_range
)

results$review_flag <- ifelse(
  results$review_flag == "review" |
    results$worst_case_continuity < 0.50 |
    results$threshold_pass_rate < 0.60,
  "review",
  "acceptable"
)

results$rank <- rank(-results$resilience_adjusted_score, ties.method = "min")
results <- results[order(results$rank), ]

write.csv(systems, file.path(tables_dir, "cascading_risk_system_profiles.csv"), row.names = FALSE)
write.csv(scenario_performance, file.path(tables_dir, "cascading_risk_scenario_performance.csv"), row.names = FALSE)
write.csv(scenario_summary, file.path(tables_dir, "cascading_risk_scenario_summary.csv"), row.names = FALSE)
write.csv(results, file.path(tables_dir, "cascading_risk_decision_results.csv"), row.names = FALSE)

png(file.path(figures_dir, "cascade_risk_scores.png"), width = 1200, height = 800)
barplot(
  results$cascade_risk_score,
  names.arg = results$system,
  las = 2,
  main = "Cascade Risk Score by System",
  ylab = "Risk score"
)
grid()
dev.off()

png(file.path(figures_dir, "worst_case_service_continuity.png"), width = 1200, height = 800)
barplot(
  results$worst_case_continuity,
  names.arg = results$system,
  las = 2,
  main = "Worst-Case Service Continuity",
  ylab = "Continuity"
)
grid()
dev.off()

print(results)
