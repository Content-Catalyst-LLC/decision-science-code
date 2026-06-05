# uncertainty_sensitivity_profiles.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "core_principles_weight_sensitivity.csv")
if (!file.exists(path)) stop("Run core_principles_decision_science_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
out <- aggregate(revised_score ~ changed_dimension + alternative, data = x, FUN = mean)
write.csv(out, file.path(tables_dir, "uncertainty_sensitivity_profiles.csv"), row.names = FALSE)
print(head(out, 12))
