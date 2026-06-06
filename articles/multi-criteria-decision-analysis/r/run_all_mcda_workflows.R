# run_all_mcda_workflows.R
# Run all R workflows for Multi-Criteria Decision Analysis.

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
  "mcda_workflow.R",
  "weighted_score_tables.R",
  "rank_stability_tables.R",
  "sensitivity_review_tables.R",
  "criteria_contribution_reports.R",
  "mcda_review_summary.R"
)

for (script in scripts) {
  path <- file.path(r_dir, script)
  message("Running ", path)
  source(path)
}

message("All R MCDA workflows completed.")
