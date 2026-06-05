# run_all_decision_record_workflows.R
# Run all R workflows for Decision Records and Accountable Judgment.

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
  "decision_records_accountable_judgment_workflow.R",
  "record_completeness_profiles.R",
  "evidence_traceability_report.R",
  "assumption_monitoring_gaps.R",
  "accountability_review_priority.R",
  "review_trigger_tables.R"
)

for (script in scripts) {
  path <- file.path(r_dir, script)
  message("Running ", path)
  source(path)
}

message("All R decision-record workflows completed.")
