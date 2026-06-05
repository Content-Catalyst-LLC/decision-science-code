# confidence_bias_summary.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "confidence_profile_summary.csv")
if (!file.exists(path)) stop("Run probability_calibration_decision_confidence_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
x$bias_direction <- ifelse(x$calibration_gap > 0.05, "overconfident", ifelse(x$calibration_gap < -0.05, "underconfident", "well calibrated"))
write.csv(x, file.path(tables_dir, "confidence_bias_summary.csv"), row.names = FALSE)
print(x)
