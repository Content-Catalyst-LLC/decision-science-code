# satisficing_profiles.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "bounded_rationality_cycle_summary.csv")
if (!file.exists(path)) stop("Run bounded_rationality_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
out <- x[order(-x$opportunity_loss), c("cycle", "domain", "aspiration", "satisficing_option", "optimizing_option", "search_length", "opportunity_loss", "review_flag")]
write.csv(out, file.path(tables_dir, "satisficing_profiles.csv"), row.names = FALSE)
print(head(out, 25))
