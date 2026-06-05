# risk_premium_profiles.R
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
out <- aggregate(risk_premium ~ prospect, data = x, FUN = mean)
names(out) <- c("prospect", "average_risk_premium")
out <- out[order(-out$average_risk_premium), ]
write.csv(out, file.path(tables_dir, "risk_premium_profiles.csv"), row.names = FALSE)
print(out)
