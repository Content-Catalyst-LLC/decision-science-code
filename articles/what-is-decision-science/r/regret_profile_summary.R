# regret_profile_summary.R
# Base R regret profile summary.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)

if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}

tables_dir <- file.path(article_root, "outputs", "tables")
regret_path <- file.path(tables_dir, "decision_regret_matrix.csv")

if (!file.exists(regret_path)) {
  stop("Missing decision_regret_matrix.csv. Run Python workflow first.")
}

regret <- read.csv(regret_path, stringsAsFactors = FALSE)
summary <- aggregate(
  regret ~ alternative,
  data = regret,
  FUN = function(x) c(mean = mean(x), max = max(x), sd = sd(x))
)

out <- data.frame(
  alternative = summary$alternative,
  average_regret = summary$regret[, "mean"],
  maximum_regret = summary$regret[, "max"],
  regret_sd = summary$regret[, "sd"]
)

write.csv(out, file.path(tables_dir, "regret_profile_summary.csv"), row.names = FALSE)
print(out)
