# probability_sensitivity_profiles.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "probability_sensitivity_diagnostics.csv")
if (!file.exists(path)) stop("Run decision_science_vs_decision_theory_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
out <- aggregate(top_expected_value_strategy ~ shock_probability, data = x, FUN = function(v) v[1])
write.csv(x, file.path(tables_dir, "probability_sensitivity_profiles.csv"), row.names = FALSE)
print(x)
