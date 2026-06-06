# feedback_loops_delays_policy_resistance_workflow.R
# Base R workflow for feedback loops, delays, and policy resistance:
# dynamic policy scoring, scenario performance, threshold review,
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

contexts <- read.csv(file.path(article_root, "data", "synthetic_policy_contexts.csv"), stringsAsFactors = FALSE)
scenario_performance <- read.csv(file.path(article_root, "data", "synthetic_scenario_performance.csv"), stringsAsFactors = FALSE)

contexts$dynamic_policy_score <- (
  0.24 * contexts$balancing_correction -
    0.18 * contexts$reinforcing_pressure -
    0.18 * contexts$implementation_delay -
    0.18 * contexts$resistance_intensity +
    0.22 * contexts$monitoring_quality
)

contexts$review_flag <- ifelse(
  contexts$reinforcing_pressure > 0.75 |
    contexts$implementation_delay > 0.65 |
    contexts$resistance_intensity > 0.65 |
    contexts$monitoring_quality < 0.50,
  "review",
  "acceptable"
)

scenario_split <- split(scenario_performance$performance, scenario_performance$context)

scenario_summary <- data.frame(
  context = names(scenario_split),
  average_scenario_performance = as.numeric(sapply(scenario_split, mean)),
  worst_case_performance = as.numeric(sapply(scenario_split, min)),
  performance_range = as.numeric(sapply(scenario_split, function(x) max(x) - min(x))),
  threshold_pass_rate = as.numeric(sapply(scenario_split, function(x) mean(x >= 0.70))),
  stringsAsFactors = FALSE
)

results <- merge(contexts, scenario_summary, by = "context")

results$feedback_adjusted_score <- (
  0.35 * results$dynamic_policy_score +
    0.25 * results$average_scenario_performance +
    0.20 * results$worst_case_performance +
    0.20 * results$threshold_pass_rate
)

results$review_flag <- ifelse(
  results$review_flag == "review" | results$worst_case_performance < 0.60,
  "review",
  "acceptable"
)

results$rank <- rank(-results$feedback_adjusted_score, ties.method = "min")
results <- results[order(results$rank), ]

write.csv(
  contexts,
  file.path(tables_dir, "feedback_delay_policy_contexts.csv"),
  row.names = FALSE
)

write.csv(
  scenario_performance,
  file.path(tables_dir, "feedback_delay_scenario_performance.csv"),
  row.names = FALSE
)

write.csv(
  scenario_summary,
  file.path(tables_dir, "feedback_delay_scenario_summary.csv"),
  row.names = FALSE
)

write.csv(
  results,
  file.path(tables_dir, "feedback_delay_policy_results.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "feedback_delay_policy_scores.png"), width = 1200, height = 800)
barplot(
  results$feedback_adjusted_score,
  names.arg = results$context,
  las = 2,
  main = "Feedback-Adjusted Policy Score",
  ylab = "Score"
)
grid()
dev.off()

png(file.path(figures_dir, "policy_resistance_dimensions.png"), width = 1200, height = 800)
barplot(
  t(as.matrix(results[, c("reinforcing_pressure", "implementation_delay", "resistance_intensity")])),
  beside = TRUE,
  names.arg = results$context,
  las = 2,
  main = "Policy Resistance Dimensions",
  ylab = "Value"
)
legend(
  "topright",
  legend = c("Reinforcing pressure", "Implementation delay", "Resistance intensity"),
  fill = gray.colors(3)
)
grid()
dev.off()

print(results)
