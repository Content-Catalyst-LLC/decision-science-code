# behavioral_diagnostics_summary.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "domain_behavioral_decision_summary.csv")
if (!file.exists(path)) stop("Run behavioral_decision_theory_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
x$domain_review_flag <- ifelse(x$review_rate > 0.35, "review", "acceptable")
write.csv(x, file.path(tables_dir, "behavioral_diagnostics_summary.csv"), row.names = FALSE)
print(x)
