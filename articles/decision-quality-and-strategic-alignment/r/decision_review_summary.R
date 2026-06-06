# decision_review_summary.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "decision_quality_alignment_review_flags.csv")
if (!file.exists(path)) stop("Run decision_quality_strategic_alignment_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
summary <- as.data.frame(table(x$review_flag), stringsAsFactors = FALSE)
names(summary) <- c("review_flag", "n_decisions")
write.csv(summary, file.path(tables_dir, "decision_review_summary.csv"), row.names = FALSE)
print(summary)
