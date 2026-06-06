# run_all_path_dependence_workflows.R
# Run all R workflows for Path Dependence, Lock-In, and Decision Timing.

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
  "path_dependence_lock_in_decision_timing_workflow.R",
  "path_profiles.R",
  "scenario_performance.R",
  "lock_in_review_tables.R",
  "timing_summary.R"
)

for (script in scripts) {
  path <- file.path(r_dir, script)
  message("Running ", path)
  source(path)
}

message("All R path-dependence workflows completed.")
