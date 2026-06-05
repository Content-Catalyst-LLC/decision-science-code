# scenario_robustness_report.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "strategy_robustness_summary.csv")
if (!file.exists(path)) stop("Run sensitivity_analysis_scenario_comparison_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
out <- x[order(-x$robustness_score), c("strategy", "probability_weighted_score", "minimum_score", "score_range", "robustness_score")]
write.csv(out, file.path(tables_dir, "scenario_robustness_report.csv"), row.names = FALSE)
print(out)
