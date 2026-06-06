args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
script_path <- if (length(file_arg) > 0) normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE) else file.path(getwd(), "r", "crisis_review_tables.R")
article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
tables_dir <- file.path(article_root, "outputs", "tables")
x <- read.csv(file.path(tables_dir, "crisis_response_decision_results.csv"), stringsAsFactors = FALSE)
out <- x[x$review_flag == "review", ]
write.csv(out, file.path(tables_dir, "crisis_review_tables.csv"), row.names = FALSE)
print(out)
