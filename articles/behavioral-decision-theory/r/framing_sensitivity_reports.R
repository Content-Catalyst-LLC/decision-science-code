# framing_sensitivity_reports.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "behavioral_decision_theory_cases.csv")
if (!file.exists(path)) stop("Run behavioral_decision_theory_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
out <- x[order(-x$frame_sensitivity_index), c("case_id", "domain", "gain_frame_score", "loss_frame_score", "frame_sensitivity_index", "review_flag")]
write.csv(out, file.path(tables_dir, "framing_sensitivity_reports.csv"), row.names = FALSE)
print(head(out, 25))
