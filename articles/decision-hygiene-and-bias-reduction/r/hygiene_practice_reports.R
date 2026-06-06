# hygiene_practice_reports.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "hygiene_practice_summary.csv")
if (!file.exists(path)) stop("Run decision_hygiene_bias_reduction_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
x$practice_review_flag <- ifelse(x$mse_reduction < 0 | x$review_rate > 0.50, "review", "acceptable")
write.csv(x, file.path(tables_dir, "hygiene_practice_reports.csv"), row.names = FALSE)
print(x)
