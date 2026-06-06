# value_of_information_review_summary.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "voi_summary_metrics.csv")
if (!file.exists(path)) stop("Run value_of_information_when_to_wait_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
write.csv(x, file.path(tables_dir, "value_of_information_review_summary.csv"), row.names = FALSE)
print(x)
