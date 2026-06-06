# run_all_regret_minimax_workflows.R
# Run all R workflows for Regret Analysis and Minimax Decision Rules.

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
  "regret_analysis_minimax_decision_rules_workflow.R",
  "regret_tables.R",
  "minimax_rule_tables.R",
  "maximin_rule_tables.R",
  "threshold_review_tables.R",
  "decision_rule_summary.R"
)

for (script in scripts) {
  path <- file.path(r_dir, script)
  message("Running ", path)
  source(path)
}

message("All R regret and minimax workflows completed.")
