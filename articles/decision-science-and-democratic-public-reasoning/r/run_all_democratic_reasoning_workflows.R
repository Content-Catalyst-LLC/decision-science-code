# run_all_democratic_reasoning_workflows.R
# Run all R workflows for Decision Science and Democratic Public Reasoning.

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
  "democratic_public_reasoning_workflow.R",
  "democratic_process_profiles.R",
  "public_trust_review.R",
  "contestability_review_tables.R",
  "democratic_public_reasoning_summary.R"
)

for (script in scripts) {
  path <- file.path(r_dir, script)
  message("Running ", path)
  source(path)
}

message("All R democratic-public-reasoning workflows completed.")
