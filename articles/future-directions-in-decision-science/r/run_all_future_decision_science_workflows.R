# run_all_future_decision_science_workflows.R
# Run all R workflows for Future Directions in Decision Science.

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
  "future_directions_decision_science_workflow.R",
  "future_pathway_profiles.R",
  "failure_risk_review.R",
  "adaptive_capacity_review.R",
  "future_decision_science_summary.R"
)

for (script in scripts) {
  path <- file.path(r_dir, script)
  message("Running ", path)
  source(path)
}

message("All R future decision-science workflows completed.")
