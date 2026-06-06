# confidence_gap_reports.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "heuristic_judgment_cases.csv")
if (!file.exists(path)) stop("Run heuristics_cognitive_biases_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
x$confidence_flag <- ifelse(x$confidence_gap > 0.12, "overconfident", ifelse(x$confidence_gap < -0.12, "underconfident", "acceptable"))
out <- x[order(-abs(x$confidence_gap)), c("case_id", "domain", "bias_profile", "judged_probability", "confidence", "confidence_gap", "confidence_flag")]
write.csv(out, file.path(tables_dir, "confidence_gap_reports.csv"), row.names = FALSE)
print(head(out, 25))
