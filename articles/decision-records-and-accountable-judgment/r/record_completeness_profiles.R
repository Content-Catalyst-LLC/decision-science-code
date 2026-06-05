# record_completeness_profiles.R
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
out <- x[order(-x$decision_record_quality), c("record_id", "decision_context", "decision_record_quality", "minimum_component_score", "quality_profile")]
write.csv(out, file.path(tables_dir, "record_completeness_profiles.csv"), row.names = FALSE)
print(out)
