args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
article_root <- if (length(file_arg) > 0) normalizePath(file.path(dirname(normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)), ".."), mustWork = TRUE) else getwd()
r_dir <- file.path(article_root, "r")
scripts <- c("robust_decision_making_workflow.R", "robustness_tables.R", "regret_tables.R", "vulnerability_tables.R", "threshold_review_tables.R", "robust_decision_review_summary.R")
for (script in scripts) { path <- file.path(r_dir, script); message("Running ", path); source(path) }
message("All R robust decision workflows completed.")
