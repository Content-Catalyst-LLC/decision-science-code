# run_all_stakeholder_legitimacy_workflows.R
# Run all R workflows for Stakeholder Values and Decision Legitimacy.

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
  "stakeholder_values_decision_legitimacy_workflow.R",
  "stakeholder_scores.R",
  "burden_tables.R",
  "procedural_legitimacy_tables.R",
  "threshold_review_tables.R",
  "legitimacy_summary.R"
)

for (script in scripts) {
  path <- file.path(r_dir, script)
  message("Running ", path)
  source(path)
}

message("All R stakeholder legitimacy workflows completed.")
