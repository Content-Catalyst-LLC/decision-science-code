# probability_assumption_audit.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
probability_sets <- read.csv(file.path(article_root, "data", "synthetic_probability_sets.csv"), stringsAsFactors = FALSE)
quality_map <- c(high = 1.0, medium = 0.65, low = 0.35)
probability_sets$quality_score <- quality_map[probability_sets$quality]
out <- aggregate(quality_score ~ prospect, data = probability_sets, FUN = mean)
names(out) <- c("prospect", "average_probability_quality")
out <- out[order(out$average_probability_quality), ]
write.csv(out, file.path(tables_dir, "probability_assumption_audit.csv"), row.names = FALSE)
print(out)
