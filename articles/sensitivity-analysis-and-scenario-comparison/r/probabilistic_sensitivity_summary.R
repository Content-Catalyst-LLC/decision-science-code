# probabilistic_sensitivity_summary.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "probabilistic_sensitivity_summary.csv")
if (!file.exists(path)) {
  message("Python probabilistic summary not found; creating R placeholder from robustness summary.")
  base_path <- file.path(tables_dir, "strategy_robustness_summary.csv")
  if (!file.exists(base_path)) stop("Run main workflows first.")
  x <- read.csv(base_path, stringsAsFactors = FALSE)
  out <- data.frame(
    strategy = x$strategy,
    probability_weighted_score = x$probability_weighted_score,
    robustness_score = x$robustness_score,
    stringsAsFactors = FALSE
  )
} else {
  out <- read.csv(path, stringsAsFactors = FALSE)
}
write.csv(out, file.path(tables_dir, "probabilistic_sensitivity_summary_r.csv"), row.names = FALSE)
print(out)
