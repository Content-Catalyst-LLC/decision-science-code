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
path <- file.path(tables_dir, "judgment_under_uncertainty_cases.csv")
if (!file.exists(path)) stop("Run judgment_under_uncertainty_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
out <- x[order(-abs(x$confidence_gap)), c("case_id", "domain", "forecast_probability", "confidence", "confidence_gap", "confidence_flag", "review_flag")]
write.csv(out, file.path(tables_dir, "confidence_error_reports.csv"), row.names = FALSE)
print(head(out, 25))
