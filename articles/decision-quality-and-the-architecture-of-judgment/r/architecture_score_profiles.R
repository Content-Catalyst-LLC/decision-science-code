# architecture_score_profiles.R
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
out <- x[order(-x$architecture_score), c("alternative", "decision_quality_score", "minimum_component_score", "balance_score", "architecture_score", "process_profile")]
write.csv(out, file.path(tables_dir, "architecture_score_profiles.csv"), row.names = FALSE)
print(out)
