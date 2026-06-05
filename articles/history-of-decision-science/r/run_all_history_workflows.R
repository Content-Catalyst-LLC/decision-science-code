# run_all_history_workflows.R
# Run all R workflows for The History of Decision Science.

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
  "history_of_decision_science_workflow.R",
  "expected_utility_history_profiles.R",
  "subjective_probability_profiles.R",
  "regret_and_robustness_history.R",
  "bounded_rationality_summary.R",
  "historical_rank_visualization.R"
)

for (script in scripts) {
  path <- file.path(r_dir, script)
  message("Running ", path)
  source(path)
}

message("All R history workflows completed.")
