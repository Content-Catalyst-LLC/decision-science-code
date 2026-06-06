# run_all_judgment_workflows.R
# Run all R workflows for Judgment Under Uncertainty.

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
  "judgment_under_uncertainty_workflow.R",
  "calibration_review_tables.R",
  "confidence_error_reports.R",
  "bayesian_revision_profiles.R",
  "evidence_quality_diagnostics.R",
  "judgment_review_tables.R"
)

for (script in scripts) {
  path <- file.path(r_dir, script)
  message("Running ", path)
  source(path)
}

message("All R judgment workflows completed.")
