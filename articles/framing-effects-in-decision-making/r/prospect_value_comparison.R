# prospect_value_comparison.R
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
out <- data.frame(
  case_id = x$case_id,
  domain = x$domain,
  ev_gain_difference = x$ev_risky_gain - x$ev_sure_gain,
  prospect_gain_difference = x$prospect_risky_gain - x$prospect_sure_gain,
  ev_loss_difference = x$ev_risky_loss - x$ev_sure_loss,
  prospect_loss_difference = x$prospect_risky_loss - x$prospect_sure_loss,
  stringsAsFactors = FALSE
)
write.csv(out, file.path(tables_dir, "prospect_value_comparison.csv"), row.names = FALSE)
print(head(out, 25))
