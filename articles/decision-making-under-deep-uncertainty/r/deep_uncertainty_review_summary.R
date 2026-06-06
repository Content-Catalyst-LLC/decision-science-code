# deep_uncertainty_review_summary.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "dmdu_robustness_results_by_profile.csv")
if (!file.exists(path)) stop("Run decision_making_under_deep_uncertainty_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
summary <- as.data.frame(table(x$profile, x$review_flag), stringsAsFactors = FALSE)
names(summary) <- c("profile", "review_flag", "n_strategies")
write.csv(summary, file.path(tables_dir, "deep_uncertainty_review_summary.csv"), row.names = FALSE)
print(summary)
