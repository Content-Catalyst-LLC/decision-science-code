# run_all_forecasting_workflows.R
# Run all R workflows for Forecasting and Decision Support.

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
  "forecasting_decision_support_workflow.R",
  "forecast_accuracy_profiles.R",
  "calibration_reliability_tables.R",
  "threshold_decision_tables.R",
  "forecast_value_reports.R",
  "horizon_degradation_summary.R"
)

for (script in scripts) {
  path <- file.path(r_dir, script)
  message("Running ", path)
  source(path)
}

message("All R forecasting workflows completed.")
