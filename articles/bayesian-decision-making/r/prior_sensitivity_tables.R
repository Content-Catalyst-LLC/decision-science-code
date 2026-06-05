# prior_sensitivity_tables.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "bayesian_prior_sensitivity.csv")
if (!file.exists(path)) stop("Run bayesian_decision_making_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
out <- aggregate(utility_difference ~ case, data = x, FUN = function(v) max(v) - min(v))
names(out) <- c("case", "utility_difference_sensitivity_range")
out <- out[order(-out$utility_difference_sensitivity_range), ]
write.csv(out, file.path(tables_dir, "prior_sensitivity_tables.csv"), row.names = FALSE)
print(out)
