# planning_bias_tables.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "overconfidence_decision_cases.csv")
if (!file.exists(path)) stop("Run overconfidence_decision_failure_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
out <- x[order(-x$duration_planning_error), c("case_id", "domain", "estimated_duration", "actual_duration", "duration_planning_error", "estimated_cost", "actual_cost", "cost_planning_error", "review_flag")]
write.csv(out, file.path(tables_dir, "planning_bias_tables.csv"), row.names = FALSE)
print(head(out, 25))
