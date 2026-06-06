# debiasing_review_tables.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "debiasing_review_queue.csv")
if (!file.exists(path)) stop("Run heuristics_cognitive_biases_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
summary <- as.data.frame(table(x$bias_profile), stringsAsFactors = FALSE)
names(summary) <- c("bias_profile", "review_count")
summary <- summary[order(-summary$review_count), ]
write.csv(summary, file.path(tables_dir, "debiasing_review_tables.csv"), row.names = FALSE)
print(summary)
