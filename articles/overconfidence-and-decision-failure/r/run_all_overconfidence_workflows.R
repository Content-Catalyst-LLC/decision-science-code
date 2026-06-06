# run_all_overconfidence_workflows.R
# Run all R workflows for Overconfidence and Decision Failure.

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
  "overconfidence_decision_failure_workflow.R",
  "calibration_review_tables.R",
  "confidence_error_reports.R",
  "interval_coverage_diagnostics.R",
  "planning_bias_tables.R",
  "overconfidence_review_summary.R"
)

for (script in scripts) {
  path <- file.path(r_dir, script)
  message("Running ", path)
  source(path)
}

message("All R overconfidence workflows completed.")
