# posterior_utility_report.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "bayesian_decision_profiles.csv")
if (!file.exists(path)) stop("Run bayesian_decision_making_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
out <- x[order(-x$utility_difference), c("case", "action_utility", "wait_utility", "utility_difference", "recommended_action")]
write.csv(out, file.path(tables_dir, "posterior_utility_report.csv"), row.names = FALSE)
print(out)
