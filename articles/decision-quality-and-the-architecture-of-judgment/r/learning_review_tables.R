# learning_review_tables.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
triggers <- read.csv(file.path(article_root, "data", "synthetic_review_triggers.csv"), stringsAsFactors = FALSE)
write.csv(triggers, file.path(tables_dir, "learning_review_triggers.csv"), row.names = FALSE)
print(triggers)
