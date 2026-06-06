# decision_science_healthcare_workflow.R
# Base R workflow for healthcare decision science:
# treatment scoring, scenario robustness, preference review,
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

treatments <- read.csv(file.path(article_root, "data", "synthetic_treatment_profiles.csv"), stringsAsFactors = FALSE)
scenario_performance <- read.csv(file.path(article_root, "data", "synthetic_scenario_performance.csv"), stringsAsFactors = FALSE)

treatments$treatment_value_score <- (
  0.30 * treatments$expected_benefit -
    0.18 * treatments$adverse_event_risk -
    0.14 * treatments$cost_burden +
    0.18 * treatments$patient_preference_fit +
    0.10 * treatments$equity_score +
    0.10 * treatments$implementation_feasibility
)

treatments$review_flag <- ifelse(
  treatments$adverse_event_risk > 0.25 |
    treatments$patient_preference_fit < 0.60 |
    treatments$equity_score < 0.55 |
    treatments$implementation_feasibility < 0.55,
  "review",
  "acceptable"
)

scenario_split <- split(scenario_performance$performance, scenario_performance$treatment)

scenario_summary <- data.frame(
  treatment = names(scenario_split),
  average_performance = as.numeric(sapply(scenario_split, mean)),
  worst_case_performance = as.numeric(sapply(scenario_split, min)),
  performance_range = as.numeric(sapply(scenario_split, function(x) max(x) - min(x))),
  threshold_pass_rate = as.numeric(sapply(scenario_split, function(x) mean(x >= 0.65))),
  stringsAsFactors = FALSE
)

results <- merge(treatments, scenario_summary, by = "treatment")

results$robust_healthcare_score <- (
  0.34 * results$treatment_value_score +
    0.24 * results$average_performance +
    0.22 * results$worst_case_performance +
    0.14 * results$threshold_pass_rate -
    0.06 * results$performance_range
)

results$review_flag <- ifelse(
  results$review_flag == "review" |
    results$worst_case_performance < 0.50 |
    results$threshold_pass_rate < 0.60,
  "review",
  "acceptable"
)

results$rank <- rank(-results$robust_healthcare_score, ties.method = "min")
results <- results[order(results$rank), ]

write.csv(treatments, file.path(tables_dir, "healthcare_treatment_profiles.csv"), row.names = FALSE)
write.csv(scenario_performance, file.path(tables_dir, "healthcare_scenario_performance.csv"), row.names = FALSE)
write.csv(scenario_summary, file.path(tables_dir, "healthcare_scenario_summary.csv"), row.names = FALSE)
write.csv(results, file.path(tables_dir, "healthcare_decision_results.csv"), row.names = FALSE)

png(file.path(figures_dir, "healthcare_robust_scores.png"), width = 1200, height = 800)
barplot(
  results$robust_healthcare_score,
  names.arg = results$treatment,
  las = 2,
  main = "Robust Healthcare Treatment Score",
  ylab = "Score"
)
grid()
dev.off()

png(file.path(figures_dir, "healthcare_worst_case_performance.png"), width = 1200, height = 800)
barplot(
  results$worst_case_performance,
  names.arg = results$treatment,
  las = 2,
  main = "Worst-Case Treatment Performance",
  ylab = "Worst-case performance"
)
grid()
dev.off()

print(results)
