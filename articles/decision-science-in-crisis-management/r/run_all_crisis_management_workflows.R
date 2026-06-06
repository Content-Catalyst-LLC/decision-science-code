args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
script_path <- if (length(file_arg) > 0) normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE) else file.path(getwd(), "r", "run_all_crisis_management_workflows.R")
article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
r_dir <- file.path(article_root, "r")

scripts <- c(
  "decision_science_crisis_management_workflow.R",
  "crisis_response_profiles.R",
  "scenario_performance.R",
  "crisis_review_tables.R",
  "crisis_management_summary.R"
)

for (script in scripts) {
  path <- file.path(r_dir, script)
  message("Running ", path)
  source(path)
}

message("All R crisis-management workflows completed.")
