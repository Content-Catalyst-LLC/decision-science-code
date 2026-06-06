# bias_noise_summary_tables.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "domain_decision_hygiene_summary.csv")
if (!file.exists(path)) stop("Run decision_hygiene_bias_reduction_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
out <- x[order(-x$mse_reduction), c("domain", "pre_bias", "post_bias", "bias_reduction", "pre_noise", "post_noise", "noise_reduction", "mse_reduction")]
write.csv(out, file.path(tables_dir, "bias_noise_summary_tables.csv"), row.names = FALSE)
print(out)
