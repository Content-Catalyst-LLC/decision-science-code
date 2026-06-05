# calibration_gap_reports.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "domain_calibration_summary.csv")
if (!file.exists(path)) stop("Run probability_calibration_decision_confidence_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
x$calibration_flag <- ifelse(abs(x$calibration_gap) > 0.08, "review", "acceptable")
out <- x[order(-abs(x$calibration_gap)), ]
write.csv(out, file.path(tables_dir, "calibration_gap_reports.csv"), row.names = FALSE)
print(out)
