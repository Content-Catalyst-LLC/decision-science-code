# robustness_and_adaptability_summary.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "core_principles_decision_profiles.csv")
if (!file.exists(path)) stop("Run core_principles_decision_science_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
x$robust_adaptive_index <- 0.5 * x$robustness + 0.5 * x$adaptability
out <- x[order(-x$robust_adaptive_index), c("alternative", "robustness", "adaptability", "robust_adaptive_index")]
write.csv(out, file.path(tables_dir, "robustness_and_adaptability_summary.csv"), row.names = FALSE)
print(out)
