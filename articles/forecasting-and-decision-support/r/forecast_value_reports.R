# forecast_value_reports.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "domain_forecast_decision_support_summary.csv")
if (!file.exists(path)) stop("Run forecasting_decision_support_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
x <- x[order(-x$average_forecast_value_proxy), ]
write.csv(x, file.path(tables_dir, "forecast_value_reports.csv"), row.names = FALSE)
print(x)
