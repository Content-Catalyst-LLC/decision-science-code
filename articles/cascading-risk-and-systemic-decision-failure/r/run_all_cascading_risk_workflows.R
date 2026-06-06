# run_all_cascading_risk_workflows.R
# Run all R workflows for Cascading Risk and Systemic Decision Failure.

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
  "cascading_risk_systemic_failure_workflow.R",
  "system_profiles.R",
  "scenario_performance.R",
  "cascade_review_tables.R",
  "resilience_summary.R"
)

for (script in scripts) {
  path <- file.path(r_dir, script)
  message("Running ", path)
  source(path)
}

message("All R cascading-risk workflows completed.")
