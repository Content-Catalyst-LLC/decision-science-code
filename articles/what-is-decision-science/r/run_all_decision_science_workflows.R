# run_all_decision_science_workflows.R
# Run all R workflows for What Is Decision Science?

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
  "decision_science_summary_reporting.R",
  "mcda_tradeoff_profiles.R",
  "sensitivity_weight_diagnostics.R",
  "regret_profile_summary.R",
  "robustness_visualization.R",
  "decision_record_tables.R"
)

for (script in scripts) {
  path <- file.path(r_dir, script)
  message("Running ", path)
  source(path)
}

message("All R decision science workflows completed.")
