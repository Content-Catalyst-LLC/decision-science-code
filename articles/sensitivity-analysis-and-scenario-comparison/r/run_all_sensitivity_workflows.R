# run_all_sensitivity_workflows.R
# Run all R workflows for Sensitivity Analysis and Scenario Comparison.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)

if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}

r_dir <- file.path(article_root, "r")

scripts <- c(
  "sensitivity_analysis_scenario_comparison_workflow.R",
  "ranking_stability_profiles.R",
  "scenario_robustness_report.R",
  "threshold_analysis_tables.R",
  "regret_summary_tables.R",
  "probabilistic_sensitivity_summary.R"
)

for (script in scripts) {
  path <- file.path(r_dir, script)
  message("Running ", path)
  source(path)
}

message("All R sensitivity-analysis workflows completed.")
