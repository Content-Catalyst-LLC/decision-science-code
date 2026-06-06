# run_all_decision_hygiene_workflows.R
# Run all R workflows for Decision Hygiene and Bias Reduction.

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
  "decision_hygiene_bias_reduction_workflow.R",
  "bias_noise_summary_tables.R",
  "calibration_review_tables.R",
  "hygiene_practice_reports.R",
  "evidence_quality_review.R",
  "decision_hygiene_review_summary.R"
)

for (script in scripts) {
  path <- file.path(r_dir, script)
  message("Running ", path)
  source(path)
}

message("All R decision hygiene workflows completed.")
