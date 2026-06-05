# run_all_core_principles_workflows.R
# Run all R workflows for Core Principles of Decision Science.

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
  "core_principles_decision_science_workflow.R",
  "mcda_principle_profiles.R",
  "uncertainty_sensitivity_profiles.R",
  "robustness_and_adaptability_summary.R",
  "decision_record_completeness_report.R",
  "principle_alignment_visualization.R"
)

for (script in scripts) {
  path <- file.path(r_dir, script)
  message("Running ", path)
  source(path)
}

message("All R core principles workflows completed.")
