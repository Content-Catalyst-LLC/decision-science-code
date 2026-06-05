# run_all_expected_utility_workflows.R
# Run all R workflows for Expected Value and Expected Utility.

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
  "expected_value_expected_utility_workflow.R",
  "expected_value_profiles.R",
  "utility_curve_sensitivity.R",
  "certainty_equivalent_report.R",
  "risk_premium_profiles.R",
  "probability_assumption_audit.R"
)

for (script in scripts) {
  path <- file.path(r_dir, script)
  message("Running ", path)
  source(path)
}

message("All R expected-utility workflows completed.")
