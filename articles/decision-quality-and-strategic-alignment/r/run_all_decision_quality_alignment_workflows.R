# run_all_decision_quality_alignment_workflows.R
# Run all R workflows for Decision Quality and Strategic Alignment.

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
  "decision_quality_strategic_alignment_workflow.R",
  "decision_quality_tables.R",
  "strategic_alignment_tables.R",
  "alignment_drift_tables.R",
  "performance_summary_tables.R",
  "decision_review_summary.R"
)

for (script in scripts) {
  path <- file.path(r_dir, script)
  message("Running ", path)
  source(path)
}

message("All R decision quality and alignment workflows completed.")
