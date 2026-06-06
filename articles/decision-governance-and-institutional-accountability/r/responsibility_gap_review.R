# responsibility_gap_review.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "accountability_records.csv")
if (!file.exists(path)) stop("Run decision_governance_accountability_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
out <- x[x$gap_review_flag == "review", ]
write.csv(out, file.path(tables_dir, "responsibility_gap_review.csv"), row.names = FALSE)
print(out)
