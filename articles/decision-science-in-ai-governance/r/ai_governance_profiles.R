# ai_governance_profiles.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "ai_governance_option_profiles.csv")
if (!file.exists(path)) stop("Run decision_science_ai_governance_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
write.csv(x, file.path(tables_dir, "ai_governance_profiles.csv"), row.names = FALSE)
print(x)
