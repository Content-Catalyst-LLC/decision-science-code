# run_all_bayesian_workflows.R
# Run all R workflows for Bayesian Decision-Making.

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
  "bayesian_decision_making_workflow.R",
  "posterior_profiles.R",
  "prior_sensitivity_tables.R",
  "posterior_utility_report.R",
  "value_of_information_tables.R",
  "evidence_quality_summary.R"
)

for (script in scripts) {
  path <- file.path(r_dir, script)
  message("Running ", path)
  source(path)
}

message("All R Bayesian workflows completed.")
