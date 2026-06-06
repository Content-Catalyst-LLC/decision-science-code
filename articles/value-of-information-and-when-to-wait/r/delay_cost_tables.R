# delay_cost_tables.R
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
out <- x[x$metric %in% c("information_cost", "delay_cost", "net_value_of_information", "net_value_of_waiting"), ]
write.csv(out, file.path(tables_dir, "delay_cost_tables.csv"), row.names = FALSE)
print(out)
