# evidence_traceability_report.R
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
out <- x[order(x$traceability_share), c("record_id", "decision_context", "traceability_share", "claim_evidence_quality")]
write.csv(out, file.path(tables_dir, "evidence_traceability_report.csv"), row.names = FALSE)
print(out)
