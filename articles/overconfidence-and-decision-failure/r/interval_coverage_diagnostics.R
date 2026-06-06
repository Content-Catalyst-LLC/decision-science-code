# interval_coverage_diagnostics.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "domain_overconfidence_summary.csv")
if (!file.exists(path)) stop("Run overconfidence_decision_failure_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
x$duration_coverage_flag <- ifelse(x$duration_interval_coverage < 0.80, "overprecise", "acceptable")
x$cost_coverage_flag <- ifelse(x$cost_interval_coverage < 0.80, "overprecise", "acceptable")
write.csv(x, file.path(tables_dir, "interval_coverage_diagnostics.csv"), row.names = FALSE)
print(x)
