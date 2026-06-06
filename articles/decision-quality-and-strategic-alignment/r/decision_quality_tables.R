# decision_quality_tables.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "decision_quality_alignment_profiles.csv")
if (!file.exists(path)) stop("Run decision_quality_strategic_alignment_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
out <- x[order(-x$decision_quality_score), c("decision", "decision_quality_score", "strategic_alignment_score", "implementation_readiness", "combined_decision_value", "rank")]
write.csv(out, file.path(tables_dir, "decision_quality_tables.csv"), row.names = FALSE)
print(out)
