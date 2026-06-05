# core_principles_decision_science_workflow.R
# Base R workflow for comparing alternatives across core decision-science principles.

args <- commandArgs(trailingOnly = FALSE)
file_arg <- grep("^--file=", args, value = TRUE)

if (length(file_arg) > 0) {
  script_path <- normalizePath(sub("^--file=", "", file_arg[1]), mustWork = TRUE)
  article_root <- normalizePath(file.path(dirname(script_path), ".."), mustWork = TRUE)
} else {
  article_root <- getwd()
}

setwd(article_root)

tables_dir <- file.path(article_root, "outputs", "tables")
figures_dir <- file.path(article_root, "outputs", "figures")
dir.create(tables_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(figures_dir, recursive = TRUE, showWarnings = FALSE)

alternatives <- read.csv(file.path(article_root, "data", "synthetic_principle_scores.csv"), stringsAsFactors = FALSE)
weights_table <- read.csv(file.path(article_root, "data", "synthetic_criteria_weights.csv"), stringsAsFactors = FALSE)

weights <- weights_table$weight
names(weights) <- weights_table$criterion

if (abs(sum(weights) - 1) > 1e-8) stop("Weights must sum to 1.")

dimensions <- names(weights)

alternatives$composite_decision_quality <- as.numeric(as.matrix(alternatives[, dimensions]) %*% weights)
alternatives$minimum_principle_score <- apply(alternatives[, dimensions], 1, min)
alternatives$principle_balance <- 1 - apply(alternatives[, dimensions], 1, sd)

alternatives$robust_principle_score <- (
  0.50 * alternatives$composite_decision_quality +
  0.30 * alternatives$minimum_principle_score +
  0.20 * alternatives$principle_balance
)

alternatives$decision_profile <- ifelse(
  alternatives$composite_decision_quality >= 0.84 & alternatives$minimum_principle_score >= 0.75,
  "strong integrated decision-science profile",
  ifelse(
    alternatives$robustness >= 0.85 & alternatives$systems_awareness >= 0.85,
    "strong systems and robustness profile",
    ifelse(
      alternatives$adaptability >= 0.88 & alternatives$decision_record_completeness >= 0.85,
      "strong adaptive learning profile",
      "comparison alternative"
    )
  )
)

alternatives <- alternatives[order(-alternatives$robust_principle_score), ]

write.csv(alternatives, file.path(tables_dir, "core_principles_decision_profiles.csv"), row.names = FALSE)

long_rows <- data.frame()

for (dimension in dimensions) {
  temp <- data.frame(
    alternative = alternatives$alternative,
    dimension = dimension,
    value = alternatives[[dimension]],
    stringsAsFactors = FALSE
  )
  long_rows <- rbind(long_rows, temp)
}

write.csv(long_rows, file.path(tables_dir, "core_principles_long_profiles.csv"), row.names = FALSE)

sensitivity_rows <- data.frame()

for (dimension in dimensions) {
  for (delta in c(-0.05, 0.05)) {
    revised_weights <- weights
    revised_weights[dimension] <- max(0.01, revised_weights[dimension] + delta)
    revised_weights <- revised_weights / sum(revised_weights)

    score <- as.numeric(as.matrix(alternatives[, dimensions]) %*% revised_weights)

    temp <- data.frame(
      changed_dimension = dimension,
      delta = delta,
      alternative = alternatives$alternative,
      revised_score = score,
      stringsAsFactors = FALSE
    )

    temp$top_alternative_after_change <- temp$alternative[which.max(temp$revised_score)]
    sensitivity_rows <- rbind(sensitivity_rows, temp)
  }
}

write.csv(sensitivity_rows, file.path(tables_dir, "core_principles_weight_sensitivity.csv"), row.names = FALSE)

instability_summary <- aggregate(
  top_alternative_after_change ~ changed_dimension,
  data = sensitivity_rows,
  FUN = function(x) length(unique(x))
)

names(instability_summary) <- c("dimension", "number_of_top_rank_outcomes")

write.csv(instability_summary, file.path(tables_dir, "core_principles_instability_summary.csv"), row.names = FALSE)

png(file.path(figures_dir, "composite_decision_quality.png"), width = 1200, height = 800)
barplot(alternatives$composite_decision_quality, names.arg = alternatives$alternative, las = 2, main = "Composite Decision Quality by Alternative", ylab = "Composite score")
grid()
dev.off()

png(file.path(figures_dir, "robust_principle_score.png"), width = 1200, height = 800)
barplot(alternatives$robust_principle_score, names.arg = alternatives$alternative, las = 2, main = "Robust Principle Score by Alternative", ylab = "Robust principle score")
grid()
dev.off()

png(file.path(figures_dir, "minimum_principle_score.png"), width = 1200, height = 800)
barplot(alternatives$minimum_principle_score, names.arg = alternatives$alternative, las = 2, main = "Minimum Principle Score by Alternative", ylab = "Minimum score across principles")
grid()
dev.off()

print(alternatives)
print(instability_summary)
