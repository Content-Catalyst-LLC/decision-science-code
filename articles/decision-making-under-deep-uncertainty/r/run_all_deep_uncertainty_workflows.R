# run_all_deep_uncertainty_workflows.R
# Run all R workflows for Decision-Making Under Deep Uncertainty.

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
  "decision_making_under_deep_uncertainty_workflow.R",
  "ambiguity_profile_tables.R",
  "regret_tables.R",
  "vulnerability_tables.R",
  "adaptive_strategy_tables.R",
  "deep_uncertainty_review_summary.R"
)

for (script in scripts) {
  path <- file.path(r_dir, script)
  message("Running ", path)
  source(path)
}

message("All R deep uncertainty workflows completed.")
