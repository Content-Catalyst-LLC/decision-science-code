# adaptive_pathway_tables.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
indicators <- read.csv(file.path(article_root, "data", "synthetic_monitoring_indicators.csv"), stringsAsFactors = FALSE)
write.csv(indicators, file.path(tables_dir, "adaptive_pathway_monitoring_table.csv"), row.names = FALSE)
print(indicators)
