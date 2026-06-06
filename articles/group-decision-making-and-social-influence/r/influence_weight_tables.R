# influence_weight_tables.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "group_member_estimates.csv")
if (!file.exists(path)) stop("Run group_decision_social_influence_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
out <- x[order(x$group_id, -x$influence_weight), c("group_id", "domain", "member_id", "expertise", "status", "influence_weight")]
write.csv(out, file.path(tables_dir, "influence_weight_tables.csv"), row.names = FALSE)
print(head(out, 25))
