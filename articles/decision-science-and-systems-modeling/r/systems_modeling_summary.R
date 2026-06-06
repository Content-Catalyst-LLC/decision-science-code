# systems_modeling_summary.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "systems_modeling_decision_results.csv")
if (!file.exists(path)) stop("Run decision_science_systems_modeling_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
x <- x[order(x$systems_decision_rank), ]
write.csv(x, file.path(tables_dir, "systems_modeling_summary.csv"), row.names = FALSE)
print(x)
