# threshold_analysis_tables.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "resilience_weight_threshold_analysis.csv")
if (!file.exists(path)) stop("Run sensitivity_analysis_scenario_comparison_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
changes <- x[c(TRUE, x$winning_strategy[-1] != x$winning_strategy[-nrow(x)]), ]
write.csv(changes, file.path(tables_dir, "threshold_analysis_tables.csv"), row.names = FALSE)
print(changes)
