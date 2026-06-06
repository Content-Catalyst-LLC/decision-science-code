# gain_loss_frame_profiles.R
args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)
if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}
tables_dir <- file.path(article_root, "outputs", "tables")
path <- file.path(tables_dir, "framing_effects_choice_cases.csv")
if (!file.exists(path)) stop("Run framing_effects_decision_making_workflow.R first.")
x <- read.csv(path, stringsAsFactors = FALSE)
out <- x[, c("case_id", "domain", "gain_frame_choice", "loss_frame_choice", "frame_reversal", "frame_sensitivity_index")]
out <- out[order(-out$frame_sensitivity_index), ]
write.csv(out, file.path(tables_dir, "gain_loss_frame_profiles.csv"), row.names = FALSE)
print(head(out, 25))
