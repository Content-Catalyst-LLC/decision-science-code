# accountability_review_priority.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "decision_record_quality_summary.csv")
if (!file.exists(path)) stop("Run decision_records_accountable_judgment_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
out <- x[order(-x$review_priority_score), c("record_id", "decision_context", "review_priority_score", "review_priority", "active_review_triggers", "critical_monitoring_gaps")]
write.csv(out, file.path(tables_dir, "accountability_review_priority.csv"), row.names = FALSE)
print(out)
