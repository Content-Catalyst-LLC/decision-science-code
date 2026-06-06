# decision_science_public_policy_workflow.R
# Base R workflow for public policy decision science:
# multi-objective scoring, scenario robustness, equity review,
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

policies <- read.csv(file.path(article_root, "data", "synthetic_policy_profiles.csv"), stringsAsFactors = FALSE)
scenario_performance <- read.csv(file.path(article_root, "data", "synthetic_scenario_performance.csv"), stringsAsFactors = FALSE)

policies$policy_value_score <- (
  0.18 * policies$efficiency +
    0.22 * policies$equity +
    0.18 * policies$resilience +
    0.14 * policies$feasibility +
    0.14 * policies$legitimacy +
    0.14 * policies$implementation_capacity
)

policies$review_flag <- ifelse(
  policies$equity < 0.55 |
    policies$legitimacy < 0.55 |
    policies$implementation_capacity < 0.55,
  "review",
  "acceptable"
)

scenario_split <- split(scenario_performance$performance, scenario_performance$policy)

scenario_summary <- data.frame(
  policy = names(scenario_split),
  average_performance = as.numeric(sapply(scenario_split, mean)),
  worst_case_performance = as.numeric(sapply(scenario_split, min)),
  performance_range = as.numeric(sapply(scenario_split, function(x) max(x) - min(x))),
  threshold_pass_rate = as.numeric(sapply(scenario_split, function(x) mean(x >= 0.70))),
  stringsAsFactors = FALSE
)

results <- merge(policies, scenario_summary, by = "policy")

results$robust_policy_score <- (
  0.32 * results$policy_value_score +
    0.24 * results$average_performance +
    0.22 * results$worst_case_performance +
    0.16 * results$threshold_pass_rate -
    0.06 * results$performance_range
)

results$review_flag <- ifelse(
  results$review_flag == "review" |
    results$worst_case_performance < 0.55 |
    results$threshold_pass_rate < 0.60,
  "review",
  "acceptable"
)

results$rank <- rank(-results$robust_policy_score, ties.method = "min")
results <- results[order(results$rank), ]

write.csv(policies, file.path(tables_dir, "public_policy_package_profiles.csv"), row.names = FALSE)
write.csv(scenario_performance, file.path(tables_dir, "public_policy_scenario_performance.csv"), row.names = FALSE)
write.csv(scenario_summary, file.path(tables_dir, "public_policy_scenario_summary.csv"), row.names = FALSE)
write.csv(results, file.path(tables_dir, "public_policy_decision_results.csv"), row.names = FALSE)

png(file.path(figures_dir, "public_policy_robust_scores.png"), width = 1200, height = 800)
barplot(
  results$robust_policy_score,
  names.arg = results$policy,
  las = 2,
  main = "Robust Public Policy Decision Score",
  ylab = "Score"
)
grid()
dev.off()

png(file.path(figures_dir, "public_policy_worst_case_performance.png"), width = 1200, height = 800)
barplot(
  results$worst_case_performance,
  names.arg = results$policy,
  las = 2,
  main = "Worst-Case Policy Performance",
  ylab = "Worst-case performance"
)
grid()
dev.off()

print(results)
