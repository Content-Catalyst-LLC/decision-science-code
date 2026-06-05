# run_all_risk_analysis_workflows.R
# Run all R workflows for Risk Analysis and Probabilistic Reasoning.

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
  "risk_analysis_probabilistic_reasoning_workflow.R",
  "expected_loss_profiles.R",
  "tail_exposure_report.R",
  "stress_test_tables.R",
  "probability_quality_summary.R",
  "bayesian_update_tables.R"
)

for (script in scripts) {
  path <- file.path(r_dir, script)
  message("Running ", path)
  source(path)
}

message("All R risk-analysis workflows completed.")
