# decision_quality_strategic_alignment_workflow.R
# Base R workflow for decision quality and strategic alignment:
# process quality, strategic fit, implementation readiness,
# alignment drift, and decision review tables.

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

set.seed(42)

decisions <- read.csv(file.path(article_root, "data", "synthetic_decisions.csv"), stringsAsFactors = FALSE)
quality_data <- read.csv(file.path(article_root, "data", "synthetic_quality_dimensions.csv"), stringsAsFactors = FALSE)
alignment_data <- read.csv(file.path(article_root, "data", "synthetic_alignment_dimensions.csv"), stringsAsFactors = FALSE)
strategy_data <- read.csv(file.path(article_root, "data", "synthetic_strategy_vectors.csv"), stringsAsFactors = FALSE)

quality_dimensions <- quality_data$dimension
alignment_dimensions <- alignment_data$dimension
quality_weights <- setNames(quality_data$weight, quality_data$dimension)
alignment_weights <- setNames(alignment_data$weight, alignment_data$dimension)
strategy_vector <- setNames(strategy_data$weight, strategy_data$dimension)

if (abs(sum(quality_weights) - 1) > 1e-9) stop("Quality weights must sum to 1.")
if (abs(sum(alignment_weights) - 1) > 1e-9) stop("Alignment weights must sum to 1.")
if (abs(sum(strategy_vector) - 1) > 1e-9) stop("Strategy vector must sum to 1.")

quality_matrix <- as.matrix(decisions[, quality_dimensions])
alignment_matrix <- as.matrix(decisions[, alignment_dimensions])

decisions$decision_quality_score <- as.vector(quality_matrix %*% quality_weights)
decisions$strategic_alignment_score <- as.vector(alignment_matrix %*% alignment_weights)

decisions$combined_decision_value <- (
  0.45 * decisions$decision_quality_score +
    0.40 * decisions$strategic_alignment_score +
    0.15 * decisions$implementation_readiness
)

decisions$rank <- rank(-decisions$combined_decision_value, ties.method = "min")
decisions <- decisions[order(decisions$rank), ]

write.csv(
  decisions,
  file.path(tables_dir, "decision_quality_alignment_profiles.csv"),
  row.names = FALSE
)

write.csv(
  data.frame(dimension = names(quality_weights), weight = as.numeric(quality_weights)),
  file.path(tables_dir, "decision_quality_weights.csv"),
  row.names = FALSE
)

write.csv(
  data.frame(dimension = names(alignment_weights), weight = as.numeric(alignment_weights)),
  file.path(tables_dir, "strategic_alignment_weights.csv"),
  row.names = FALSE
)

cosine_similarity <- function(x, y) {
  sum(x * y) / (sqrt(sum(x^2)) * sqrt(sum(y^2)))
}

strategy_columns <- names(strategy_vector)

decision_vectors <- data.frame(
  decision = decisions$decision,
  decisions[, strategy_columns],
  stringsAsFactors = FALSE
)

decision_vectors$strategy_vector_alignment <- apply(
  decision_vectors[, strategy_columns],
  1,
  function(row) cosine_similarity(as.numeric(row), strategy_vector)
)

write.csv(
  decision_vectors,
  file.path(tables_dir, "strategy_vector_alignment.csv"),
  row.names = FALSE
)

periods <- 12
pattern_records <- list()

for (t in seq_len(periods)) {
  noise <- rnorm(length(strategy_vector), mean = 0, sd = 0.06)
  drift_push <- ifelse(names(strategy_vector) == "growth", 0.025 * t, -0.007 * t)
  observed_pattern <- pmax(strategy_vector + noise + drift_push, 0.01)
  observed_pattern <- observed_pattern / sum(observed_pattern)

  pattern_records[[t]] <- data.frame(
    period = t,
    growth = observed_pattern["growth"],
    resilience = observed_pattern["resilience"],
    equity = observed_pattern["equity"],
    learning = observed_pattern["learning"],
    legitimacy = observed_pattern["legitimacy"],
    alignment = cosine_similarity(observed_pattern, strategy_vector),
    strategic_drift = 1 - cosine_similarity(observed_pattern, strategy_vector),
    stringsAsFactors = FALSE
  )
}

decision_pattern <- do.call(rbind, pattern_records)

write.csv(
  decision_pattern,
  file.path(tables_dir, "decision_pattern_alignment_drift.csv"),
  row.names = FALSE
)

performance_records <- list()
performance_summary <- list()
counter <- 1

for (i in seq_len(nrow(decisions))) {
  value <- 100.0
  values <- numeric(40)

  for (cycle in seq_len(40)) {
    shock <- rnorm(1, mean = 0, sd = 1.6)
    quality_effect <- decisions$decision_quality_score[i] * runif(1, 0.4, 1.0)
    alignment_effect <- decisions$strategic_alignment_score[i] * runif(1, 0.5, 1.1)
    execution_effect <- decisions$implementation_readiness[i] * runif(1, 0.3, 0.9)
    growth_rate <- 0.50 + shock + quality_effect + alignment_effect + execution_effect
    value <- max(40, value * (1 + growth_rate / 100))
    values[cycle] <- value

    performance_records[[counter]] <- data.frame(
      decision = decisions$decision[i],
      cycle = cycle,
      performance_value = value,
      growth_rate = growth_rate,
      stringsAsFactors = FALSE
    )
    counter <- counter + 1
  }

  performance_summary[[i]] <- data.frame(
    decision = decisions$decision[i],
    final_value = values[length(values)],
    min_value = min(values),
    max_value = max(values),
    average_value = mean(values),
    volatility = sd(values),
    stringsAsFactors = FALSE
  )
}

performance_table <- do.call(rbind, performance_records)
performance_summary_table <- do.call(rbind, performance_summary)

write.csv(
  performance_table,
  file.path(tables_dir, "decision_quality_alignment_performance.csv"),
  row.names = FALSE
)

write.csv(
  performance_summary_table,
  file.path(tables_dir, "decision_quality_alignment_performance_summary.csv"),
  row.names = FALSE
)

review_flags <- merge(
  decisions[, c("decision", "decision_quality_score", "strategic_alignment_score", "implementation_readiness", "combined_decision_value", "rank")],
  decision_vectors[, c("decision", "strategy_vector_alignment")],
  by = "decision",
  all.x = TRUE
)

review_flags$review_flag <- ifelse(
  review_flags$decision_quality_score < 0.70 |
    review_flags$strategic_alignment_score < 0.70 |
    review_flags$strategy_vector_alignment < 0.85 |
    review_flags$implementation_readiness < 0.65,
  "review",
  "acceptable"
)

review_flags <- review_flags[order(review_flags$rank), ]

write.csv(
  review_flags,
  file.path(tables_dir, "decision_quality_alignment_review_flags.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "decision_quality_alignment_scores.png"), width = 1200, height = 800)
barplot(
  decisions$combined_decision_value,
  names.arg = decisions$decision,
  las = 2,
  main = "Combined Decision Quality and Strategic Alignment",
  ylab = "Combined decision value"
)
grid()
dev.off()

png(file.path(figures_dir, "quality_vs_alignment.png"), width = 1200, height = 800)
plot(
  decisions$decision_quality_score,
  decisions$strategic_alignment_score,
  xlim = c(0, 1),
  ylim = c(0, 1),
  xlab = "Decision quality score",
  ylab = "Strategic alignment score",
  main = "Decision Quality vs Strategic Alignment",
  pch = 19
)
text(
  decisions$decision_quality_score,
  decisions$strategic_alignment_score,
  labels = decisions$decision,
  pos = 4,
  cex = 0.8
)
grid()
dev.off()

png(file.path(figures_dir, "alignment_drift_over_time.png"), width = 1200, height = 800)
plot(
  decision_pattern$period,
  decision_pattern$strategic_drift,
  type = "l",
  lwd = 2,
  xlab = "Decision period",
  ylab = "Strategic drift",
  main = "Strategic Drift Across Repeated Decisions"
)
grid()
dev.off()

print(decisions)
print(decision_vectors)
print(decision_pattern)
print(review_flags)
