# run_all_decision_tree_workflows.R
# Run all R workflows for Decision Trees and Structured Choice.

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
  "decision_trees_structured_choice_workflow.R",
  "rollback_profiles.R",
  "value_of_information_report.R",
  "probability_sensitivity_profiles.R",
  "threshold_analysis_tables.R",
  "regret_summary_tables.R"
)

for (script in scripts) {
  path <- file.path(r_dir, script)
  message("Running ", path)
  source(path)
}

message("All R decision-tree workflows completed.")
