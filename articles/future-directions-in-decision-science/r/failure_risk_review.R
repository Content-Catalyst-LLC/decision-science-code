# failure_risk_review.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "future_decision_science_pathways.csv")
if (!file.exists(path)) stop("Run future_directions_decision_science_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
out <- x[order(-x$failure_risk), c("pathway", "failure_risk", "governance_maturity", "adaptive_capacity", "review_flag")]
write.csv(out, file.path(tables_dir, "failure_risk_review.csv"), row.names = FALSE)
print(out)
