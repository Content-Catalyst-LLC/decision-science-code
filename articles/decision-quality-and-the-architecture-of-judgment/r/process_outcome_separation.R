# process_outcome_separation.R
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
out <- x[, c("alternative", "decision_quality_score", "architecture_score", "mean_outcome", "favorable_outcome_rate", "outcome_bias_warning")]
write.csv(out, file.path(tables_dir, "process_outcome_separation.csv"), row.names = FALSE)
print(out)
