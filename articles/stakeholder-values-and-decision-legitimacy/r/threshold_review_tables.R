# threshold_review_tables.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "decision_legitimacy_results.csv")
if (!file.exists(path)) stop("Run stakeholder_values_decision_legitimacy_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
out <- x[x$review_flag == "review", ]
write.csv(out, file.path(tables_dir, "threshold_review_tables.csv"), row.names = FALSE)
print(out)
