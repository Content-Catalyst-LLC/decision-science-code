# regret_profile_diagnostics.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "regret_profile_table.csv")
if (!file.exists(path)) stop("Run decision_science_vs_decision_theory_workflow.R first.")
regret <- read.csv(path, stringsAsFactors = FALSE)
summary <- aggregate(regret ~ strategy, data = regret, FUN = function(x) c(mean = mean(x), max = max(x), sd = sd(x)))
out <- data.frame(strategy = summary$strategy, average_regret = summary$regret[, "mean"], maximum_regret = summary$regret[, "max"], regret_sd = summary$regret[, "sd"])
write.csv(out, file.path(tables_dir, "regret_profile_diagnostics.csv"), row.names = FALSE)
print(out)
