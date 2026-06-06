# tradeoffs_values_competing_objectives_workflow.R
# Base R workflow for trade-off analysis:
# competing objectives, weighted scoring, priority sensitivity,
# dominated alternatives, rank stability, scenario regret, and review tables.

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
objectives_data <- read.csv(file.path(article_root, "data", "synthetic_objectives.csv"), stringsAsFactors = FALSE)
weights_data <- read.csv(file.path(article_root, "data", "synthetic_weights.csv"), stringsAsFactors = FALSE)
scenario_weights_data <- read.csv(file.path(article_root, "data", "synthetic_scenario_weights.csv"), stringsAsFactors = FALSE)
stakeholder_profiles_data <- read.csv(file.path(article_root, "data", "synthetic_stakeholder_profiles.csv"), stringsAsFactors = FALSE)

objectives <- objectives_data$objective
base_weights <- setNames(weights_data$weight, weights_data$objective)

if (abs(sum(base_weights) - 1) > 1e-9) {
  stop("Weights must sum to 1.")
}

score_matrix <- as.matrix(alternatives[, objectives])
base_scores <- as.vector(score_matrix %*% base_weights)

base_results <- data.frame(
  alternative = alternatives$alternative,
  composite_score = base_scores,
  rank = rank(-base_scores, ties.method = "min"),
  stringsAsFactors = FALSE
)

base_results <- base_results[order(base_results$rank), ]

write.csv(
  alternatives,
  file.path(tables_dir, "tradeoff_objective_profiles.csv"),
  row.names = FALSE
)

write.csv(
  data.frame(objective = names(base_weights), weight = as.numeric(base_weights)),
  file.path(tables_dir, "tradeoff_base_weights.csv"),
  row.names = FALSE
)

write.csv(
  base_results,
  file.path(tables_dir, "tradeoff_base_results.csv"),
  row.names = FALSE
)

dominance_rows <- list()
counter <- 1

for (i in seq_len(nrow(alternatives))) {
  for (j in seq_len(nrow(alternatives))) {
    if (i != j) {
      a_scores <- as.numeric(alternatives[i, objectives])
      b_scores <- as.numeric(alternatives[j, objectives])
      b_dominates_a <- all(b_scores >= a_scores) && any(b_scores > a_scores)

      dominance_rows[[counter]] <- data.frame(
        alternative_a = alternatives$alternative[i],
        alternative_b = alternatives$alternative[j],
        b_dominates_a = b_dominates_a,
        stringsAsFactors = FALSE
      )
      counter <- counter + 1
    }
  }
}

dominance_table <- do.call(rbind, dominance_rows)

dominated_summary <- do.call(
  rbind,
  lapply(
    split(dominance_table, dominance_table$alternative_a),
    function(x) {
      data.frame(
        alternative = unique(x$alternative_a),
        dominated_by_any = any(x$b_dominates_a),
        dominator_count = sum(x$b_dominates_a),
        stringsAsFactors = FALSE
      )
    }
  )
)

write.csv(
  dominated_summary,
  file.path(tables_dir, "tradeoff_dominated_options.csv"),
  row.names = FALSE
)

n_sim <- 3000
alpha <- base_weights * 70
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
  file.path(tables_dir, "tradeoff_priority_sensitivity_simulations.csv"),
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
  file.path(tables_dir, "tradeoff_rank_stability_summary.csv"),
  row.names = FALSE
)

scenario_names <- unique(scenario_weights_data$scenario)
regret_records <- list()
counter <- 1

for (scenario_name in scenario_names) {
  scenario_subset <- scenario_weights_data[scenario_weights_data$scenario == scenario_name, ]
  weights <- setNames(scenario_subset$weight, scenario_subset$objective)

  if (abs(sum(weights) - 1) > 1e-9) {
    stop(paste("Scenario weights must sum to 1:", scenario_name))
  }

  scenario_scores <- as.vector(score_matrix %*% weights)
  best_score <- max(scenario_scores)
  scenario_ranks <- rank(-scenario_scores, ties.method = "min")

  for (i in seq_along(scenario_scores)) {
    regret_records[[counter]] <- data.frame(
      scenario = scenario_name,
      alternative = alternatives$alternative[i],
      scenario_score = scenario_scores[i],
      regret = best_score - scenario_scores[i],
      rank = scenario_ranks[i],
      stringsAsFactors = FALSE
    )
    counter <- counter + 1
  }
}

regret_table <- do.call(rbind, regret_records)

write.csv(
  regret_table,
  file.path(tables_dir, "tradeoff_scenario_regret_table.csv"),
  row.names = FALSE
)

regret_summary <- do.call(
  rbind,
  lapply(
    split(regret_table, regret_table$alternative),
    function(x) {
      data.frame(
        alternative = unique(x$alternative),
        average_regret = mean(x$regret),
        max_regret = max(x$regret),
        average_rank = mean(x$rank),
        worst_rank = max(x$rank),
        stringsAsFactors = FALSE
      )
    }
  )
)

regret_summary <- regret_summary[order(regret_summary$max_regret, regret_summary$average_regret), ]

write.csv(
  regret_summary,
  file.path(tables_dir, "tradeoff_regret_summary.csv"),
  row.names = FALSE
)

profile_outputs <- list()
profile_names <- unique(stakeholder_profiles_data$profile)

for (profile_name in profile_names) {
  profile_subset <- stakeholder_profiles_data[stakeholder_profiles_data$profile == profile_name, ]
  weights <- setNames(profile_subset$weight, profile_subset$objective)

  if (abs(sum(weights) - 1) > 1e-9) {
    stop(paste("Stakeholder profile weights must sum to 1:", profile_name))
  }

  profile_scores <- as.vector(score_matrix %*% weights)

  profile_outputs[[profile_name]] <- data.frame(
    profile = profile_name,
    alternative = alternatives$alternative,
    profile_score = profile_scores,
    rank = rank(-profile_scores, ties.method = "min"),
    stringsAsFactors = FALSE
  )
}

stakeholder_profile_results <- do.call(rbind, profile_outputs)
stakeholder_profile_results <- stakeholder_profile_results[order(stakeholder_profile_results$profile, stakeholder_profile_results$rank), ]

write.csv(
  stakeholder_profile_results,
  file.path(tables_dir, "tradeoff_stakeholder_profile_results.csv"),
  row.names = FALSE
)

criterion_contributions <- data.frame(
  alternative = alternatives$alternative,
  score_matrix * matrix(base_weights, nrow = nrow(score_matrix), ncol = length(base_weights), byrow = TRUE),
  check.names = FALSE,
  stringsAsFactors = FALSE
)

criterion_contributions$total_score <- rowSums(criterion_contributions[, objectives])

write.csv(
  criterion_contributions,
  file.path(tables_dir, "tradeoff_objective_contributions.csv"),
  row.names = FALSE
)

review_flags <- merge(base_results, rank_stability, by = "alternative", all.x = TRUE)
review_flags <- merge(review_flags, regret_summary, by = "alternative", all.x = TRUE)
review_flags <- merge(review_flags, dominated_summary, by = "alternative", all.x = TRUE)

review_flags$review_flag <- ifelse(
  review_flags$dominated_by_any |
    review_flags$best_rank_rate < 0.25 |
    review_flags$rank_volatility > 1.25 |
    review_flags$max_regret > 0.20,
  "review",
  "acceptable"
)

review_flags <- review_flags[order(review_flags$rank), ]

write.csv(
  review_flags,
  file.path(tables_dir, "tradeoff_review_flags.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "tradeoff_base_scores.png"), width = 1200, height = 800)
barplot(
  base_results$composite_score,
  names.arg = base_results$alternative,
  las = 2,
  main = "Composite Trade-Off Scores",
  ylab = "Composite score"
)
grid()
dev.off()

png(file.path(figures_dir, "tradeoff_rank_stability.png"), width = 1200, height = 800)
barplot(
  rank_stability$best_rank_rate,
  names.arg = rank_stability$alternative,
  las = 2,
  main = "Rank Stability Across Priority Simulations",
  ylab = "Share of simulations ranked first"
)
grid()
dev.off()

png(file.path(figures_dir, "tradeoff_regret_summary.png"), width = 1200, height = 800)
barplot(
  regret_summary$max_regret,
  names.arg = regret_summary$alternative,
  las = 2,
  main = "Maximum Regret Across Value Scenarios",
  ylab = "Maximum regret"
)
grid()
dev.off()

print(base_results)
print(rank_stability)
print(regret_summary)
print(review_flags)
