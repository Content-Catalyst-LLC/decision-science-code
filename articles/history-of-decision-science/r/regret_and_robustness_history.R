# regret_and_robustness_history.R
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
out <- x[order(x$minimax_regret_rank, x$robustness_rank), c("strategy", "maximum_regret", "minimax_regret_rank", "robustness_share", "robustness_rank", "historical_profile")]
write.csv(out, file.path(tables_dir, "regret_and_robustness_history.csv"), row.names = FALSE)
print(out)
