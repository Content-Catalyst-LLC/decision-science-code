# historical_rank_visualization.R
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
path <- file.path(tables_dir, "historical_paradigm_comparison.csv")
if (!file.exists(path)) stop("Run history_of_decision_science_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
rank_matrix <- t(as.matrix(x[, c("emv_rank", "eu_rank", "subjective_eu_rank", "minimax_regret_rank", "robustness_rank")]))
png(file.path(figures_dir, "historical_rank_comparison.png"), width = 1200, height = 800)
barplot(rank_matrix, beside = TRUE, names.arg = x$strategy, las = 2, main = "Rank Comparison Across Historical Decision Paradigms", ylab = "Rank")
legend("topright", legend = rownames(rank_matrix), bty = "n")
grid()
dev.off()
print(x[, c("strategy", "emv_rank", "eu_rank", "subjective_eu_rank", "minimax_regret_rank", "robustness_rank")])
