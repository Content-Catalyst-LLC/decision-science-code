# confidence_error_reports.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "overconfidence_decision_cases.csv")
if (!file.exists(path)) stop("Run overconfidence_decision_failure_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
out <- x[order(-x$confidence_error), c("case_id", "domain", "forecast_probability", "confidence", "accuracy_proxy", "confidence_error", "confidence_flag", "review_flag")]
write.csv(out, file.path(tables_dir, "confidence_error_reports.csv"), row.names = FALSE)
print(head(out, 25))
