# run_all_decision_theory_science_workflows.R
# Run all R workflows for Decision Science vs. Decision Theory.

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
  "decision_science_vs_decision_theory_workflow.R",
  "normative_criteria_comparison.R",
  "regret_profile_diagnostics.R",
  "robustness_sensitivity_analysis.R",
  "probability_sensitivity_profiles.R",
  "decision_criteria_visualization.R"
)

for (script in scripts) {
  path <- file.path(r_dir, script)
  message("Running ", path)
  source(path)
}

message("All R decision theory/science workflows completed.")
