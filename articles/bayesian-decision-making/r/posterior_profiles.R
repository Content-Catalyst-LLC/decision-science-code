# posterior_profiles.R
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
out <- x[order(-x$posterior), c("case", "prior", "posterior", "bayes_factor", "recommended_action")]
write.csv(out, file.path(tables_dir, "posterior_profiles.csv"), row.names = FALSE)
print(out)
