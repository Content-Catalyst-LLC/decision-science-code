# run_all_resilience_long_horizon_workflows.R
# Run all R workflows for Resilience, Adaptation, and Long-Horizon Decisions.

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
  "resilience_adaptation_long_horizon_workflow.R",
  "strategy_profiles.R",
  "scenario_performance.R",
  "threshold_review_tables.R",
  "resilience_summary.R"
)

for (script in scripts) {
  path <- file.path(r_dir, script)
  message("Running ", path)
  source(path)
}

message("All R resilience long-horizon workflows completed.")
