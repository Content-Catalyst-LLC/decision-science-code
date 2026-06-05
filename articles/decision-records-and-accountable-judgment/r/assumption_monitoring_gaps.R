# assumption_monitoring_gaps.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "decision_record_assumption_audit.csv")
if (!file.exists(path)) stop("Run decision_records_accountable_judgment_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
out <- x[order(-x$assumption_risk), c("assumption_id", "record_id", "assumption", "confidence", "criticality", "assumption_risk", "monitoring_gap")]
write.csv(out, file.path(tables_dir, "assumption_monitoring_gaps.csv"), row.names = FALSE)
print(out)
