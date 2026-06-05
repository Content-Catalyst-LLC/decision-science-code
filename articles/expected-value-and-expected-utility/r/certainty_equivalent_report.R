# certainty_equivalent_report.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "risk_aversion_sensitivity.csv")
if (!file.exists(path)) stop("Run expected_value_expected_utility_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
out <- aggregate(certainty_equivalent ~ prospect, data = x, FUN = mean)
names(out) <- c("prospect", "average_certainty_equivalent")
out <- out[order(-out$average_certainty_equivalent), ]
write.csv(out, file.path(tables_dir, "certainty_equivalent_report.csv"), row.names = FALSE)
print(out)
