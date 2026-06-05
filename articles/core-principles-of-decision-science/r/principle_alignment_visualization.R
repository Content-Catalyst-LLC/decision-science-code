# principle_alignment_visualization.R
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
path <- file.path(tables_dir, "core_principles_long_profiles.csv")
if (!file.exists(path)) stop("Run core_principles_decision_science_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)

avg <- aggregate(value ~ dimension, data = x, FUN = mean)

png(file.path(figures_dir, "average_principle_alignment.png"), width = 1200, height = 800)
barplot(avg$value, names.arg = avg$dimension, las = 2, main = "Average Principle Alignment", ylab = "Average score")
grid()
dev.off()

print(avg)
