# decision_criteria_visualization.R
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
path <- file.path(tables_dir, "decision_criteria_comparison.csv")
if (!file.exists(path)) stop("Run decision_science_vs_decision_theory_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)

png(file.path(figures_dir, "criteria_rank_comparison.png"), width = 1200, height = 800)
mat <- t(as.matrix(x[, c("ev_rank", "minimax_regret_rank", "robustness_rank")]))
barplot(mat, beside = TRUE, names.arg = x$strategy, las = 2, main = "Rank Comparison Across Decision Criteria", ylab = "Rank")
legend("topright", legend = rownames(mat), bty = "n")
grid()
dev.off()

print(x[, c("strategy", "ev_rank", "minimax_regret_rank", "robustness_rank")])
