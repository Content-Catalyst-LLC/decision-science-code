# run_all_bounded_rationality_workflows.R
# Run all R workflows for Bounded Rationality.

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
  "bounded_rationality_workflow.R",
  "satisficing_profiles.R",
  "search_cost_tables.R",
  "adaptive_aspiration_reports.R",
  "domain_constraint_diagnostics.R",
  "bounded_rationality_review_tables.R"
)

for (script in scripts) {
  path <- file.path(r_dir, script)
  message("Running ", path)
  source(path)
}

message("All R bounded rationality workflows completed.")
