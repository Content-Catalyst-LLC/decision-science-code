# stakeholder_values_decision_legitimacy_workflow.R
# Base R workflow for stakeholder values and decision legitimacy:
# stakeholder-specific scores, burden analysis, procedural legitimacy,
# threshold checks, decision legitimacy index, and decision records.

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

alternatives <- read.csv(file.path(article_root, "data", "synthetic_alternatives.csv"), stringsAsFactors = FALSE)
criteria_data <- read.csv(file.path(article_root, "data", "synthetic_criteria.csv"), stringsAsFactors = FALSE)
stakeholders <- read.csv(file.path(article_root, "data", "synthetic_stakeholders.csv"), stringsAsFactors = FALSE)
weights <- read.csv(file.path(article_root, "data", "synthetic_value_weights.csv"), stringsAsFactors = FALSE)
burdens <- read.csv(file.path(article_root, "data", "synthetic_burdens.csv"), stringsAsFactors = FALSE)
procedure <- read.csv(file.path(article_root, "data", "synthetic_procedure_scores.csv"), stringsAsFactors = FALSE)
procedure_weights_data <- read.csv(file.path(article_root, "data", "synthetic_procedure_weights.csv"), stringsAsFactors = FALSE)

criteria <- criteria_data$criterion
procedure_weights <- setNames(procedure_weights_data$weight, procedure_weights_data$criterion)

if (abs(sum(procedure_weights) - 1) > 1e-9) {
  stop("Procedure weights must sum to 1.")
}

for (stakeholder in unique(weights$stakeholder)) {
  stakeholder_total <- sum(weights$weight[weights$stakeholder == stakeholder])
  if (abs(stakeholder_total - 1) > 1e-9) {
    stop(paste("Stakeholder weights must sum to 1 for", stakeholder))
  }
}

stakeholder_score_rows <- list()
counter <- 1

for (i in seq_len(nrow(alternatives))) {
  alt <- alternatives[i, ]

  for (stakeholder in stakeholders$stakeholder) {
    stakeholder_weights <- weights[weights$stakeholder == stakeholder, ]
    stakeholder_weights <- stakeholder_weights[match(criteria, stakeholder_weights$criterion), ]

    score <- sum(as.numeric(alt[, criteria]) * stakeholder_weights$weight)
    stakeholder_info <- stakeholders[stakeholders$stakeholder == stakeholder, ]

    stakeholder_score_rows[[counter]] <- data.frame(
      alternative = alt$alternative,
      stakeholder = stakeholder,
      stakeholder_score = score,
      importance = stakeholder_info$importance,
      minimum_threshold = stakeholder_info$minimum_threshold,
      passes_threshold = score >= stakeholder_info$minimum_threshold,
      stringsAsFactors = FALSE
    )

    counter <- counter + 1
  }
}

stakeholder_scores <- do.call(rbind, stakeholder_score_rows)
stakeholder_scores$weighted_score <- stakeholder_scores$stakeholder_score * stakeholder_scores$importance

aggregate_scores <- aggregate(
  weighted_score ~ alternative,
  data = stakeholder_scores,
  FUN = sum
)

names(aggregate_scores)[2] <- "aggregate_stakeholder_score"

threshold_summary <- aggregate(
  passes_threshold ~ alternative,
  data = stakeholder_scores,
  FUN = function(x) mean(as.numeric(x))
)

names(threshold_summary)[2] <- "stakeholder_threshold_pass_rate"

min_score_summary <- aggregate(
  stakeholder_score ~ alternative,
  data = stakeholder_scores,
  FUN = min
)

names(min_score_summary)[2] <- "minimum_stakeholder_score"

max_burden <- aggregate(
  burden ~ alternative,
  data = burdens,
  FUN = max
)

names(max_burden)[2] <- "maximum_stakeholder_burden"

avg_burden <- aggregate(
  burden ~ alternative,
  data = burdens,
  FUN = mean
)

names(avg_burden)[2] <- "average_stakeholder_burden"

procedure$procedural_score <- as.vector(
  as.matrix(procedure[, names(procedure_weights)]) %*% procedure_weights
)

results <- merge(aggregate_scores, threshold_summary, by = "alternative")
results <- merge(results, min_score_summary, by = "alternative")
results <- merge(results, max_burden, by = "alternative")
results <- merge(results, avg_burden, by = "alternative")
results <- merge(results, procedure[, c("alternative", "procedural_score")], by = "alternative")

results$decision_legitimacy_index <- (
  0.40 * results$aggregate_stakeholder_score +
    0.24 * results$procedural_score +
    0.18 * results$stakeholder_threshold_pass_rate +
    0.10 * results$minimum_stakeholder_score -
    0.08 * results$maximum_stakeholder_burden
)

results$review_flag <- ifelse(
  results$stakeholder_threshold_pass_rate < 0.80 |
    results$maximum_stakeholder_burden > 0.50 |
    results$procedural_score < 0.65,
  "review",
  "acceptable"
)

results$rank <- rank(-results$decision_legitimacy_index, ties.method = "min")
results <- results[order(results$rank), ]

write.csv(
  alternatives,
  file.path(tables_dir, "stakeholder_alternative_scores.csv"),
  row.names = FALSE
)

write.csv(
  weights,
  file.path(tables_dir, "stakeholder_value_weights.csv"),
  row.names = FALSE
)

write.csv(
  stakeholder_scores,
  file.path(tables_dir, "stakeholder_scores_by_group.csv"),
  row.names = FALSE
)

write.csv(
  burdens,
  file.path(tables_dir, "stakeholder_burden_table.csv"),
  row.names = FALSE
)

write.csv(
  procedure,
  file.path(tables_dir, "procedural_legitimacy_scores.csv"),
  row.names = FALSE
)

write.csv(
  results,
  file.path(tables_dir, "decision_legitimacy_results.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "decision_legitimacy_index_by_alternative.png"), width = 1200, height = 800)
barplot(
  results$decision_legitimacy_index,
  names.arg = results$alternative,
  las = 2,
  main = "Decision Legitimacy Index by Alternative",
  ylab = "Decision legitimacy index"
)
grid()
dev.off()

png(file.path(figures_dir, "maximum_stakeholder_burden.png"), width = 1200, height = 800)
barplot(
  results$maximum_stakeholder_burden,
  names.arg = results$alternative,
  las = 2,
  main = "Maximum Stakeholder Burden by Alternative",
  ylab = "Maximum burden"
)
grid()
dev.off()

print(results)
print(stakeholder_scores)
