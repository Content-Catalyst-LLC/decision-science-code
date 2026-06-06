# run_all_tradeoff_workflows.R
# Run all R workflows for Trade-Offs, Values, and Competing Objectives.

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
  "tradeoffs_values_competing_objectives_workflow.R",
  "weighted_objective_tables.R",
  "dominance_review_tables.R",
  "rank_stability_tables.R",
  "scenario_regret_tables.R",
  "tradeoff_review_summary.R"
)

for (script in scripts) {
  path <- file.path(r_dir, script)
  message("Running ", path)
  source(path)
}

message("All R trade-off workflows completed.")
