# normative_criteria_comparison.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "decision_criteria_comparison.csv")
if (!file.exists(path)) stop("Run decision_science_vs_decision_theory_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
out <- x[order(x$ev_rank), c("strategy", "expected_value", "expected_utility", "ev_rank", "eu_rank")]
write.csv(out, file.path(tables_dir, "normative_criteria_comparison.csv"), row.names = FALSE)
print(out)
