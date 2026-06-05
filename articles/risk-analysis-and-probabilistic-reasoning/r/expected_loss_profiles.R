# expected_loss_profiles.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "risk_profile_summary.csv")
if (!file.exists(path)) stop("Run risk_analysis_probabilistic_reasoning_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
out <- x[order(x$expected_loss), c("strategy", "mean_return", "expected_loss", "risk_adjusted_score")]
write.csv(out, file.path(tables_dir, "expected_loss_profiles.csv"), row.names = FALSE)
print(out)
