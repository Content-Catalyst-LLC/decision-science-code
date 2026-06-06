# maximin_rule_tables.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "regret_decision_rule_comparison.csv")
if (!file.exists(path)) stop("Run regret_analysis_minimax_decision_rules_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
x <- x[order(x$maximin_rank), c("strategy", "maximin_value", "best_case", "performance_range", "maximin_rank", "review_flag")]
write.csv(x, file.path(tables_dir, "maximin_rule_tables.csv"), row.names = FALSE)
print(x)
