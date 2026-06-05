# utility_curve_sensitivity.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "risk_aversion_sensitivity.csv")
if (!file.exists(path)) stop("Run expected_value_expected_utility_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
out <- x[order(x$risk_aversion, x$expected_utility_rank), c("risk_aversion", "prospect", "expected_utility", "expected_utility_rank")]
write.csv(out, file.path(tables_dir, "utility_curve_sensitivity.csv"), row.names = FALSE)
print(head(out, 15))
