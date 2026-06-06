# consensus_pressure_diagnostics.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "group_decision_summary.csv")
if (!file.exists(path)) stop("Run group_decision_social_influence_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
out <- x[order(-x$consensus_pressure), c("group_id", "domain", "consensus_pressure", "influence_concentration", "collective_error", "review_flag")]
write.csv(out, file.path(tables_dir, "consensus_pressure_diagnostics.csv"), row.names = FALSE)
print(head(out, 25))
