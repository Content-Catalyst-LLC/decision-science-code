# option_value_summary.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
params <- read.csv(file.path(article_root, "data", "synthetic_ambiguity_parameters.csv"), stringsAsFactors = FALSE)
params$option_value_proxy <- 0.60 * params$reversibility + 0.40 * (1 - params$ambiguity)
out <- params[order(-params$option_value_proxy), c("strategy", "reversibility", "ambiguity", "option_value_proxy")]
write.csv(out, file.path(tables_dir, "option_value_summary.csv"), row.names = FALSE)
print(out)
