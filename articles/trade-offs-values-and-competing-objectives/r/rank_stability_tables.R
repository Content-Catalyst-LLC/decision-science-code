# rank_stability_tables.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "tradeoff_rank_stability_summary.csv")
if (!file.exists(path)) stop("Run tradeoffs_values_competing_objectives_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
x <- x[order(-x$best_rank_rate, x$average_rank), ]
write.csv(x, file.path(tables_dir, "rank_stability_tables.csv"), row.names = FALSE)
print(x)
