# run_all_feedback_delay_workflows.R
# Run all R workflows for Feedback Loops, Delays, and Policy Resistance.

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
  "feedback_loops_delays_policy_resistance_workflow.R",
  "policy_context_profiles.R",
  "scenario_performance.R",
  "threshold_review_tables.R",
  "feedback_delay_summary.R"
)

for (script in scripts) {
  path <- file.path(r_dir, script)
  message("Running ", path)
  source(path)
}

message("All R feedback-delay workflows completed.")
