# evidence_quality_review.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "decision_hygiene_cases.csv")
if (!file.exists(path)) stop("Run decision_hygiene_bias_reduction_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
out <- x[x$evidence_quality == "low" & x$decision_stakes == "high", c("case_id", "domain", "bias_source", "hygiene_practice", "evidence_quality", "decision_stakes", "review_flag")]
write.csv(out, file.path(tables_dir, "evidence_quality_review.csv"), row.names = FALSE)
print(head(out, 25))
