# decision_record_tables.R
# Summarize decision record outputs.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)

if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}

records_dir <- file.path(article_root, "outputs", "decision_records")
tables_dir <- file.path(article_root, "outputs", "tables")
record_path <- file.path(records_dir, "decision_record.json")

if (!file.exists(record_path)) {
  stop("Missing decision_record.json. Run Python workflow first.")
}

record_summary <- data.frame(
  record_file = "decision_record.json",
  status = "created",
  path = record_path,
  stringsAsFactors = FALSE
)

write.csv(record_summary, file.path(tables_dir, "decision_record_tables.csv"), row.names = FALSE)
print(record_summary)
