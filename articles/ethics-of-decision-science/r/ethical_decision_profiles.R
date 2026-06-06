args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
script_path <- if (length(file_arg) > 0) normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE) else ""
article_root <- if (script_path != "") normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE) else getwd()
tables_dir <- file.path(article_root, "outputs", "tables")
x <- read.csv(file.path(tables_dir, "ethical_decision_results.csv"), stringsAsFactors = FALSE)
write.csv(x, file.path(tables_dir, "ethical_decision_profiles.csv"), row.names = FALSE)
print(x)
