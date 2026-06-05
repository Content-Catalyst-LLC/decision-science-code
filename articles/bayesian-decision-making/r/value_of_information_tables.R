# value_of_information_tables.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "bayesian_value_of_information_proxy.csv")
if (!file.exists(path)) stop("Run bayesian_decision_making_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
x <- x[order(-x$expected_value_of_sample_information_proxy), ]
write.csv(x, file.path(tables_dir, "value_of_information_tables.csv"), row.names = FALSE)
print(x)
