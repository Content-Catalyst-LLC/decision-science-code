# mcda_tradeoff_profiles.R
# Base R MCDA trade-off summary.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)

if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}

tables_dir <- file.path(article_root, "outputs", "tables")
mcda_path <- file.path(tables_dir, "decision_mcda_scores.csv")

if (!file.exists(mcda_path)) {
  stop("Missing decision_mcda_scores.csv. Run Python workflow first.")
}

mcda <- read.csv(mcda_path, stringsAsFactors = FALSE)
mcda <- mcda[order(-mcda$mcda_score), ]
write.csv(mcda, file.path(tables_dir, "mcda_tradeoff_profiles.csv"), row.names = FALSE)
print(mcda)
