# run_all_behavioral_decision_workflows.R
# Run all R workflows for Behavioral Decision Theory.

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
  "behavioral_decision_theory_workflow.R",
  "prospect_theory_profiles.R",
  "probability_weighting_tables.R",
  "framing_sensitivity_reports.R",
  "loss_aversion_review_tables.R",
  "behavioral_diagnostics_summary.R"
)

for (script in scripts) {
  path <- file.path(r_dir, script)
  message("Running ", path)
  source(path)
}

message("All R behavioral decision workflows completed.")
