# adaptive_aspiration_reports.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "adaptive_aspiration_path.csv")
if (!file.exists(path)) stop("Run bounded_rationality_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
x$aspiration_change <- c(NA, diff(x$aspiration))
write.csv(x, file.path(tables_dir, "adaptive_aspiration_reports.csv"), row.names = FALSE)
print(tail(x, 20))
