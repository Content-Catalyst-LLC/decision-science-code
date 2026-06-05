# ambiguity_penalty_diagnostics.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "ambiguity_sensitivity_diagnostics.csv")
if (!file.exists(path)) stop("Run why_uncertainty_changes_decision_making_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
out <- aggregate(ambiguity_adjusted_score ~ ambiguity_lambda + top_strategy_at_lambda, data = x, FUN = max)
write.csv(out, file.path(tables_dir, "ambiguity_penalty_diagnostics.csv"), row.names = FALSE)
print(head(out, 12))
