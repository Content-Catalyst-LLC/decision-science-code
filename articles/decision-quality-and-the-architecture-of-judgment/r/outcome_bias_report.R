# outcome_bias_report.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "decision_quality_diagnostic_report.csv")
if (!file.exists(path)) stop("Run decision_quality_architecture_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
out <- x[order(x$outcome_bias_warning), c("alternative", "process_profile", "favorable_outcome_rate", "outcome_bias_warning")]
write.csv(out, file.path(tables_dir, "outcome_bias_report.csv"), row.names = FALSE)
print(out)
