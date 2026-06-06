# run_all_bias_workflows.R
# Run all R workflows for Heuristics and Cognitive Biases.

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
  "heuristics_cognitive_biases_workflow.R",
  "bias_profile_summary.R",
  "calibration_error_tables.R",
  "confidence_gap_reports.R",
  "domain_bias_diagnostics.R",
  "debiasing_review_tables.R"
)

for (script in scripts) {
  path <- file.path(r_dir, script)
  message("Running ", path)
  source(path)
}

message("All R bias workflows completed.")
