# tail_exposure_report.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "risk_profile_summary.csv")
if (!file.exists(path)) stop("Run risk_analysis_probabilistic_reasoning_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
out <- x[order(x$conditional_value_at_risk_5pct), c("strategy", "value_at_risk_5pct", "conditional_value_at_risk_5pct", "downside_breach_probability")]
write.csv(out, file.path(tables_dir, "tail_exposure_report.csv"), row.names = FALSE)
print(out)
