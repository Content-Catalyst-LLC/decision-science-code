# adaptive_decision_pathways_workflow.R
# Base R workflow for adaptive decision pathways:
# pathway scoring, scenario performance, trigger review,
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

pathways <- read.csv(file.path(article_root, "data", "synthetic_pathway_profiles.csv"), stringsAsFactors = FALSE)
scenario_performance <- read.csv(file.path(article_root, "data", "synthetic_scenario_performance.csv"), stringsAsFactors = FALSE)

pathways$adaptive_pathway_score <- (
  0.20 * pathways$initial_performance +
    0.18 * pathways$flexibility +
    0.16 * pathways$monitoring_quality +
    0.16 * pathways$trigger_clarity -
    0.12 * pathways$switching_cost +
    0.18 * pathways$fallback_strength
)

pathways$review_flag <- ifelse(
  pathways$trigger_clarity < 0.45 |
    pathways$monitoring_quality < 0.45 |
    pathways$switching_cost > 0.70 |
    pathways$fallback_strength < 0.45,
  "review",
  "acceptable"
)

scenario_split <- split(scenario_performance$performance, scenario_performance$pathway)

scenario_summary <- data.frame(
  pathway = names(scenario_split),
  average_performance = as.numeric(sapply(scenario_split, mean)),
  worst_case_performance = as.numeric(sapply(scenario_split, min)),
  performance_range = as.numeric(sapply(scenario_split, function(x) max(x) - min(x))),
  threshold_pass_rate = as.numeric(sapply(scenario_split, function(x) mean(x >= 0.70))),
  stringsAsFactors = FALSE
)

results <- merge(pathways, scenario_summary, by = "pathway")

results$robust_adaptive_score <- (
  0.30 * results$adaptive_pathway_score +
    0.24 * results$average_performance +
    0.22 * results$worst_case_performance +
    0.18 * results$threshold_pass_rate -
    0.06 * results$performance_range
)

results$review_flag <- ifelse(
  results$review_flag == "review" |
    results$worst_case_performance < 0.60 |
    results$threshold_pass_rate < 0.60,
  "review",
  "acceptable"
)

results$rank <- rank(-results$robust_adaptive_score, ties.method = "min")
results <- results[order(results$rank), ]

write.csv(pathways, file.path(tables_dir, "adaptive_pathway_profiles.csv"), row.names = FALSE)
write.csv(scenario_performance, file.path(tables_dir, "adaptive_pathway_scenario_performance.csv"), row.names = FALSE)
write.csv(scenario_summary, file.path(tables_dir, "adaptive_pathway_scenario_summary.csv"), row.names = FALSE)
write.csv(results, file.path(tables_dir, "adaptive_pathway_decision_results.csv"), row.names = FALSE)

png(file.path(figures_dir, "adaptive_pathway_scores.png"), width = 1200, height = 800)
barplot(
  results$robust_adaptive_score,
  names.arg = results$pathway,
  las = 2,
  main = "Robust Adaptive Pathway Score",
  ylab = "Score"
)
grid()
dev.off()

png(file.path(figures_dir, "adaptive_pathway_worst_case_performance.png"), width = 1200, height = 800)
barplot(
  results$worst_case_performance,
  names.arg = results$pathway,
  las = 2,
  main = "Worst-Case Pathway Performance",
  ylab = "Worst-case performance"
)
grid()
dev.off()

print(results)
