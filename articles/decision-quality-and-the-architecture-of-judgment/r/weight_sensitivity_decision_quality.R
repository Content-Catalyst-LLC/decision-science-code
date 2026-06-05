# weight_sensitivity_decision_quality.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "decision_quality_weight_sensitivity.csv")
if (!file.exists(path)) stop("Run decision_quality_architecture_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
out <- aggregate(revised_decision_quality_score ~ changed_component + alternative, data = x, FUN = mean)
write.csv(out, file.path(tables_dir, "weight_sensitivity_decision_quality.csv"), row.names = FALSE)
print(head(out, 12))
