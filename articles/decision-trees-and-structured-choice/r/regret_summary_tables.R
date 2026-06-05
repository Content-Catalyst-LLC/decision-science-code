# regret_summary_tables.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "decision_tree_regret_summary.csv")
if (!file.exists(path)) stop("Run decision_trees_structured_choice_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
out <- aggregate(regret ~ strategy, data = x, FUN = mean)
names(out) <- c("strategy", "average_regret_across_states")
out <- out[order(-out$average_regret_across_states), ]
write.csv(out, file.path(tables_dir, "regret_summary_tables.csv"), row.names = FALSE)
print(out)
