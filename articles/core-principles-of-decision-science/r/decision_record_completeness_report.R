# decision_record_completeness_report.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "core_principles_decision_profiles.csv")
if (!file.exists(path)) stop("Run core_principles_decision_science_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
out <- x[order(-x$decision_record_completeness), c("alternative", "decision_record_completeness", "evidence_quality", "framing_quality")]
write.csv(out, file.path(tables_dir, "decision_record_completeness_report.csv"), row.names = FALSE)
print(out)
