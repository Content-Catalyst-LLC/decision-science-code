# ranking_stability_profiles.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "scenario_strategy_scores.csv")
if (!file.exists(path)) stop("Run sensitivity_analysis_scenario_comparison_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
out <- aggregate(scenario_rank ~ strategy, data = x, FUN = function(v) max(v) - min(v))
names(out) <- c("strategy", "rank_instability")
out <- out[order(out$rank_instability), ]
write.csv(out, file.path(tables_dir, "ranking_stability_profiles.csv"), row.names = FALSE)
print(out)
