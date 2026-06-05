# regret_and_robustness_profiles.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "uncertainty_decision_summary.csv")
if (!file.exists(path)) stop("Run why_uncertainty_changes_decision_making_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
out <- x[order(-x$robustness_share, x$maximum_regret), c("strategy", "maximum_regret", "robustness_share", "minimum_payoff", "decision_profile")]
write.csv(out, file.path(tables_dir, "regret_and_robustness_profiles.csv"), row.names = FALSE)
print(out)
