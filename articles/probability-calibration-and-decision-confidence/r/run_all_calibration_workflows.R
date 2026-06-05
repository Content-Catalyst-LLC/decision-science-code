# run_all_calibration_workflows.R
# Run all R workflows for Probability Calibration and Decision Confidence.

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
  "probability_calibration_decision_confidence_workflow.R",
  "brier_score_profiles.R",
  "reliability_tables.R",
  "calibration_gap_reports.R",
  "confidence_bias_summary.R",
  "threshold_calibration_tables.R"
)

for (script in scripts) {
  path <- file.path(r_dir, script)
  message("Running ", path)
  source(path)
}

message("All R calibration workflows completed.")
