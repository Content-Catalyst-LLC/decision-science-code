# run_all_decision_quality_workflows.R
# Run all R workflows for Decision Quality and the Architecture of Judgment.

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
  "decision_quality_architecture_workflow.R",
  "process_outcome_separation.R",
  "weight_sensitivity_decision_quality.R",
  "architecture_score_profiles.R",
  "outcome_bias_report.R",
  "learning_review_tables.R"
)

for (script in scripts) {
  path <- file.path(r_dir, script)
  message("Running ", path)
  source(path)
}

message("All R decision-quality workflows completed.")
