# mcda_workflow.R
# Base R workflow for Multi-Criteria Decision Analysis:
# weighted scoring, normalization, sensitivity, rank stability,
# and decision review tables.

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

alternatives <- read.csv(file.path(article_root, "data", "synthetic_alternatives.csv"), stringsAsFactors = FALSE)
criteria_data <- read.csv(file.path(article_root, "data", "synthetic_criteria.csv"), stringsAsFactors = FALSE)
weights_data <- read.csv(file.path(article_root, "data", "synthetic_weights.csv"), stringsAsFactors = FALSE)

criteria <- criteria_data$criterion
criterion_direction <- setNames(criteria_data$direction, criteria_data$criterion)
base_weights <- setNames(weights_data$weight, weights_data$criterion)

if (abs(sum(base_weights) - 1) > 1e-9) {
  stop("Weights must sum to 1.")
}

normalize_benefit <- function(x) {
  if (max(x) == min(x)) {
    return(rep(1, length(x)))
  }
  (x - min(x)) / (max(x) - min(x))
}

normalize_cost <- function(x) {
  if (max(x) == min(x)) {
    return(rep(1, length(x)))
  }
  (max(x) - x) / (max(x) - min(x))
}

normalized <- alternatives

for (criterion in criteria) {
  if (criterion_direction[criterion] == "cost") {
    normalized[[criterion]] <- normalize_cost(alternatives[[criterion]])
  } else {
    normalized[[criterion]] <- normalize_benefit(alternatives[[criterion]])
  }
}

score_matrix <- as.matrix(normalized[, criteria])
weighted_scores <- as.vector(score_matrix %*% base_weights)

base_results <- data.frame(
  alternative = alternatives$alternative,
  composite_score = weighted_scores,
  rank = rank(-weighted_scores, ties.method = "min"),
  stringsAsFactors = FALSE
)

base_results <- base_results[order(base_results$rank), ]

write.csv(
  alternatives,
  file.path(tables_dir, "mcda_raw_alternative_profiles.csv"),
  row.names = FALSE
)

write.csv(
  normalized,
  file.path(tables_dir, "mcda_normalized_alternative_profiles.csv"),
  row.names = FALSE
)

write.csv(
  data.frame(criterion = names(base_weights), weight = as.numeric(base_weights)),
  file.path(tables_dir, "mcda_base_weights.csv"),
  row.names = FALSE
)

write.csv(
  base_results,
  file.path(tables_dir, "mcda_base_results.csv"),
  row.names = FALSE
)

n_sim <- 3000
alpha <- base_weights * 80
simulation_records <- vector("list", n_sim)

for (i in seq_len(n_sim)) {
  random_weights <- rgamma(length(base_weights), shape = alpha, rate = 1)
  random_weights <- random_weights / sum(random_weights)

  sim_scores <- as.vector(score_matrix %*% random_weights)
  sim_ranks <- rank(-sim_scores, ties.method = "min")

  simulation_records[[i]] <- data.frame(
    simulation_id = i,
    alternative = alternatives$alternative,
    score = sim_scores,
    rank = sim_ranks,
    stringsAsFactors = FALSE
  )
}

simulation_results <- do.call(rbind, simulation_records)

write.csv(
  simulation_results,
  file.path(tables_dir, "mcda_weight_sensitivity_simulations.csv"),
  row.names = FALSE
)

rank_stability <- do.call(
  rbind,
  lapply(
    split(simulation_results, simulation_results$alternative),
    function(x) {
      data.frame(
        alternative = unique(x$alternative),
        average_score = mean(x$score),
        min_score = min(x$score),
        max_score = max(x$score),
        average_rank = mean(x$rank),
        best_rank_rate = mean(x$rank == 1),
        top_two_rate = mean(x$rank <= 2),
        rank_volatility = sd(x$rank),
        stringsAsFactors = FALSE
      )
    }
  )
)

rank_stability <- rank_stability[order(-rank_stability$best_rank_rate, rank_stability$average_rank), ]

write.csv(
  rank_stability,
  file.path(tables_dir, "mcda_rank_stability_summary.csv"),
  row.names = FALSE
)

criterion_contribution <- data.frame(
  alternative = alternatives$alternative,
  score_matrix * matrix(base_weights, nrow = nrow(score_matrix), ncol = length(base_weights), byrow = TRUE),
  check.names = FALSE,
  stringsAsFactors = FALSE
)

criterion_contribution$total_score <- rowSums(criterion_contribution[, criteria])

write.csv(
  criterion_contribution,
  file.path(tables_dir, "mcda_criterion_contributions.csv"),
  row.names = FALSE
)

stakeholder_profiles <- read.csv(file.path(article_root, "data", "synthetic_stakeholder_profiles.csv"), stringsAsFactors = FALSE)
profile_outputs <- list()
profile_names <- unique(stakeholder_profiles$profile)

for (profile_name in profile_names) {
  profile_weights <- stakeholder_profiles[stakeholder_profiles$profile == profile_name, ]
  weight_vector <- setNames(profile_weights$weight, profile_weights$criterion)

  if (abs(sum(weight_vector) - 1) > 1e-9) {
    stop(paste("Weights must sum to 1 for profile:", profile_name))
  }

  profile_scores <- as.vector(score_matrix %*% weight_vector)

  profile_outputs[[profile_name]] <- data.frame(
    profile = profile_name,
    alternative = alternatives$alternative,
    composite_score = profile_scores,
    rank = rank(-profile_scores, ties.method = "min"),
    stringsAsFactors = FALSE
  )
}

stakeholder_profile_results <- do.call(rbind, profile_outputs)
stakeholder_profile_results <- stakeholder_profile_results[order(stakeholder_profile_results$profile, stakeholder_profile_results$rank), ]

write.csv(
  stakeholder_profile_results,
  file.path(tables_dir, "mcda_stakeholder_profile_results.csv"),
  row.names = FALSE
)

outranking_rows <- list()
counter <- 1

for (a_index in seq_len(nrow(normalized))) {
  for (b_index in seq_len(nrow(normalized))) {
    if (a_index != b_index) {
      a_scores <- as.numeric(normalized[a_index, criteria])
      b_scores <- as.numeric(normalized[b_index, criteria])
      concordance <- sum(base_weights[a_scores >= b_scores])
      discordance_count <- sum((a_scores + 0.15) < b_scores)

      outranking_rows[[counter]] <- data.frame(
        alternative_a = normalized$alternative[a_index],
        alternative_b = normalized$alternative[b_index],
        concordance = concordance,
        discordance_count = discordance_count,
        a_outranks_b = concordance >= 0.60 & discordance_count == 0,
        stringsAsFactors = FALSE
      )
      counter <- counter + 1
    }
  }
}

outranking_pairs <- do.call(rbind, outranking_rows)

write.csv(
  outranking_pairs,
  file.path(tables_dir, "mcda_outranking_pairs.csv"),
  row.names = FALSE
)

review_flags <- merge(base_results, rank_stability, by = "alternative", all.x = TRUE)

review_flags$score_gap_from_leader <- max(review_flags$composite_score) - review_flags$composite_score

review_flags$review_flag <- ifelse(
  review_flags$best_rank_rate < 0.25 |
    review_flags$rank_volatility > 1.25 |
    review_flags$score_gap_from_leader < 0.03,
  "review",
  "acceptable"
)

review_flags <- review_flags[order(review_flags$rank), ]

write.csv(
  review_flags,
  file.path(tables_dir, "mcda_review_flags.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "mcda_base_scores.png"), width = 1200, height = 800)
barplot(
  base_results$composite_score,
  names.arg = base_results$alternative,
  las = 2,
  main = "MCDA Composite Scores",
  ylab = "Composite score"
)
grid()
dev.off()

png(file.path(figures_dir, "mcda_rank_stability.png"), width = 1200, height = 800)
barplot(
  rank_stability$best_rank_rate,
  names.arg = rank_stability$alternative,
  las = 2,
  main = "MCDA Rank Stability Across Weight Simulations",
  ylab = "Share of simulations ranked first"
)
grid()
dev.off()

png(file.path(figures_dir, "mcda_rank_volatility.png"), width = 1200, height = 800)
barplot(
  rank_stability$rank_volatility,
  names.arg = rank_stability$alternative,
  las = 2,
  main = "MCDA Rank Volatility",
  ylab = "Standard deviation of rank"
)
grid()
dev.off()

print(base_results)
print(rank_stability)
print(review_flags)
