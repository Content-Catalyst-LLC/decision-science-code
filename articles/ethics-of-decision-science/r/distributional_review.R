args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
script_path <- if (length(file_arg) > 0) normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE) else ""
article_root <- if (script_path != "") normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE) else getwd()
tables_dir <- file.path(article_root, "outputs", "tables")
x <- read.csv(file.path(tables_dir, "distributional_impacts.csv"), stringsAsFactors = FALSE)
summary <- aggregate(net_benefit ~ alternative, data = x, min)
names(summary)[2] <- "minimum_group_net_benefit"
write.csv(summary, file.path(tables_dir, "distributional_review.csv"), row.names = FALSE)
print(summary)
