# threshold_calibration_tables.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "decision_threshold_calibration.csv")
if (!file.exists(path)) stop("Run probability_calibration_decision_confidence_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
x$threshold_review_flag <- ifelse(abs(x$threshold_calibration_gap) > 0.08, "review", "acceptable")
write.csv(x, file.path(tables_dir, "threshold_calibration_tables.csv"), row.names = FALSE)
print(x)
