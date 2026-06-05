# robustness_visualization.R
# Base R robustness visualization.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)

if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}

tables_dir <- file.path(article_root, "outputs", "tables")
figures_dir <- file.path(article_root, "outputs", "figures")
dir.create(figures_dir, recursive = TRUE, showWarnings = FALSE)

summary_path <- file.path(tables_dir, "decision_summary.csv")

if (!file.exists(summary_path)) {
  stop("Missing decision_summary.csv. Run Python workflow first.")
}

summary <- read.csv(summary_path, stringsAsFactors = FALSE)

png(file.path(figures_dir, "robustness_visualization.png"), width = 1200, height = 750)
barplot(
  summary$robustness_share,
  names.arg = summary$alternative,
  las = 2,
  ylab = "Robustness share",
  main = "Robustness Across Alternatives"
)
grid()
dev.off()

print(summary[, c("alternative", "robustness_share")])
