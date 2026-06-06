args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
script_path <- if (length(file_arg) > 0) normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE) else ""
article_root <- if (script_path != "") normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE) else getwd()
r_dir <- file.path(article_root, "r")
scripts <- c(
  "ethics_of_decision_science_workflow.R",
  "ethical_decision_profiles.R",
  "distributional_review.R",
  "ethical_review_tables.R",
  "ethics_summary.R"
)
for (script in scripts) {
  path <- file.path(r_dir, script)
  message("Running ", path)
  source(path)
}
message("All R ethics workflows completed.")
