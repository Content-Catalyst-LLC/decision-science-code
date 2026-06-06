# search_cost_tables.R
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
x$search_cost_total <- x$search_length * x$search_cost_per_option
out <- x[order(-x$search_cost_total), c("cycle", "domain", "search_length", "search_cost_per_option", "search_cost_total", "satisficing_net_value")]
write.csv(out, file.path(tables_dir, "search_cost_tables.csv"), row.names = FALSE)
print(head(out, 25))
