# bounded_rationality_summary.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "historical_paradigm_comparison.csv")
if (!file.exists(path)) stop("Run history_of_decision_science_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
out <- x[order(-x$satisficing_share), c("strategy", "satisficing_share", "minimum_payoff", "robustness_share")]
write.csv(out, file.path(tables_dir, "bounded_rationality_summary.csv"), row.names = FALSE)
print(out)
