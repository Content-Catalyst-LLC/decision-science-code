# loss_aversion_review_tables.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "behavioral_decision_theory_cases.csv")
if (!file.exists(path)) stop("Run behavioral_decision_theory_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
out <- x[x$loss_aversion >= 2.5, c("case_id", "domain", "option_name", "loss_aversion", "prospect_score", "frame_sensitivity_index", "review_flag")]
out <- out[order(-out$loss_aversion), ]
write.csv(out, file.path(tables_dir, "loss_aversion_review_tables.csv"), row.names = FALSE)
print(head(out, 25))
