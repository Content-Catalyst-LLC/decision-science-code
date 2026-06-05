# probability_sensitivity_profiles.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "decision_tree_probability_sensitivity.csv")
if (!file.exists(path)) stop("Run decision_trees_structured_choice_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
out <- aggregate(expected_value ~ strategy, data = x, FUN = function(v) max(v) - min(v))
names(out) <- c("strategy", "expected_value_sensitivity_range")
out <- out[order(-out$expected_value_sensitivity_range), ]
write.csv(out, file.path(tables_dir, "probability_sensitivity_profiles.csv"), row.names = FALSE)
print(out)
