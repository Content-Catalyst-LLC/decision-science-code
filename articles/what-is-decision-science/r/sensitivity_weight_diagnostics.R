# sensitivity_weight_diagnostics.R
# Summarize weight sensitivity diagnostics.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)

if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}

tables_dir <- file.path(article_root, "outputs", "tables")
sensitivity_path <- file.path(tables_dir, "decision_sensitivity_analysis.csv")

if (!file.exists(sensitivity_path)) {
  stop("Missing decision_sensitivity_analysis.csv. Run Python workflow first.")
}

sensitivity <- read.csv(sensitivity_path, stringsAsFactors = FALSE)

instability <- aggregate(
  ranking_changed ~ changed_criterion,
  data = sensitivity,
  FUN = function(x) mean(as.logical(x))
)

names(instability) <- c("criterion", "ranking_instability_rate")
write.csv(instability, file.path(tables_dir, "sensitivity_weight_diagnostics.csv"), row.names = FALSE)
print(instability)
