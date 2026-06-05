# sensitivity_analysis_scenario_comparison_workflow.R
# Base R workflow for ranking stability, scenario comparison,
# threshold analysis, robustness profiles, and regret diagnostics.

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

strategies <- read.csv(file.path(article_root, "data", "synthetic_strategies.csv"), stringsAsFactors = FALSE)
scenarios <- read.csv(file.path(article_root, "data", "synthetic_scenario_weights.csv"), stringsAsFactors = FALSE)

weight_columns <- c(
  "cost_weight",
  "resilience_weight",
  "flexibility_weight",
  "implementation_weight",
  "downside_weight"
)

if (any(abs(rowSums(scenarios[, weight_columns]) - 1) > 1e-8)) {
  stop("Scenario weights must sum to 1.")
}

scenario_results <- data.frame()

for (i in seq_len(nrow(strategies))) {
  strategy <- strategies[i, ]

  for (j in seq_len(nrow(scenarios))) {
    scenario <- scenarios[j, ]

    composite_score <- (
      strategy$cost_score * scenario$cost_weight +
      strategy$resilience_score * scenario$resilience_weight +
      strategy$flexibility_score * scenario$flexibility_weight +
      strategy$implementation_score * scenario$implementation_weight +
      strategy$downside_protection * scenario$downside_weight
    )

    scenario_results <- rbind(
      scenario_results,
      data.frame(
        strategy = strategy$strategy,
        scenario = scenario$scenario,
        composite_score = composite_score,
        scenario_probability = scenario$scenario_probability,
        stringsAsFactors = FALSE
      )
    )
  }
}

scenario_results$scenario_rank <- ave(
  -scenario_results$composite_score,
  scenario_results$scenario,
  FUN = function(x) rank(x, ties.method = "min")
)

write.csv(scenario_results, file.path(tables_dir, "scenario_strategy_scores.csv"), row.names = FALSE)

robustness_summary <- do.call(
  rbind,
  lapply(
    split(scenario_results, scenario_results$strategy),
    function(x) {
      data.frame(
        strategy = unique(x$strategy),
        average_score = mean(x$composite_score),
        probability_weighted_score = sum(x$composite_score * x$scenario_probability),
        minimum_score = min(x$composite_score),
        maximum_score = max(x$composite_score),
        score_range = max(x$composite_score) - min(x$composite_score),
        average_rank = mean(x$scenario_rank),
        worst_rank = max(x$scenario_rank),
        best_rank = min(x$scenario_rank),
        rank_range = max(x$scenario_rank) - min(x$scenario_rank),
        stringsAsFactors = FALSE
      )
    }
  )
)

robustness_summary$robustness_score <- (
  0.40 * robustness_summary$probability_weighted_score +
  0.35 * robustness_summary$minimum_score -
  0.15 * robustness_summary$score_range -
  0.10 * robustness_summary$average_rank / max(robustness_summary$average_rank)
)

robustness_summary <- robustness_summary[order(-robustness_summary$robustness_score), ]

write.csv(robustness_summary, file.path(tables_dir, "strategy_robustness_summary.csv"), row.names = FALSE)

regret_rows <- data.frame()

for (scenario_name in unique(scenario_results$scenario)) {
  subset_rows <- scenario_results[scenario_results$scenario == scenario_name, ]
  best_score <- max(subset_rows$composite_score)

  regret_rows <- rbind(
    regret_rows,
    data.frame(
      strategy = subset_rows$strategy,
      scenario = subset_rows$scenario,
      composite_score = subset_rows$composite_score,
      best_scenario_score = best_score,
      regret = best_score - subset_rows$composite_score,
      stringsAsFactors = FALSE
    )
  )
}

regret_summary <- aggregate(
  regret ~ strategy,
  data = regret_rows,
  FUN = function(x) c(mean_regret = mean(x), max_regret = max(x))
)

regret_summary <- data.frame(
  strategy = regret_summary$strategy,
  average_regret = regret_summary$regret[, "mean_regret"],
  maximum_regret = regret_summary$regret[, "max_regret"],
  stringsAsFactors = FALSE
)

regret_summary <- regret_summary[order(regret_summary$maximum_regret), ]

write.csv(regret_rows, file.path(tables_dir, "scenario_regret_detail.csv"), row.names = FALSE)
write.csv(regret_summary, file.path(tables_dir, "scenario_regret_summary.csv"), row.names = FALSE)

threshold_grid <- seq(0.05, 0.60, by = 0.01)
threshold_rows <- data.frame()

for (w in threshold_grid) {
  temp <- scenarios
  temp$resilience_weight <- w

  remaining <- 1 - temp$resilience_weight
  original_other_total <- temp$cost_weight + temp$flexibility_weight + temp$implementation_weight + temp$downside_weight

  temp$cost_weight <- remaining * temp$cost_weight / original_other_total
  temp$flexibility_weight <- remaining * temp$flexibility_weight / original_other_total
  temp$implementation_weight <- remaining * temp$implementation_weight / original_other_total
  temp$downside_weight <- remaining * temp$downside_weight / original_other_total

  rows <- data.frame()

  for (i in seq_len(nrow(strategies))) {
    s <- strategies[i, ]

    for (j in seq_len(nrow(temp))) {
      sc <- temp[j, ]

      score <- (
        s$cost_score * sc$cost_weight +
        s$resilience_score * sc$resilience_weight +
        s$flexibility_score * sc$flexibility_weight +
        s$implementation_score * sc$implementation_weight +
        s$downside_protection * sc$downside_weight
      )

      rows <- rbind(
        rows,
        data.frame(
          strategy = s$strategy,
          scenario = sc$scenario,
          score = score,
          probability = sc$scenario_probability,
          stringsAsFactors = FALSE
        )
      )
    }
  }

  weighted_scores <- aggregate(score * probability ~ strategy, data = rows, FUN = sum)
  names(weighted_scores) <- c("strategy", "probability_weighted_score")
  winner <- weighted_scores$strategy[which.max(weighted_scores$probability_weighted_score)]

  threshold_rows <- rbind(
    threshold_rows,
    data.frame(
      resilience_weight = w,
      winning_strategy = winner,
      winning_score = max(weighted_scores$probability_weighted_score),
      stringsAsFactors = FALSE
    )
  )
}

write.csv(threshold_rows, file.path(tables_dir, "resilience_weight_threshold_analysis.csv"), row.names = FALSE)

png(file.path(figures_dir, "robustness_score_by_strategy.png"), width = 1200, height = 800)
barplot(
  robustness_summary$robustness_score,
  names.arg = robustness_summary$strategy,
  las = 2,
  main = "Robustness Score by Strategy",
  ylab = "Robustness score"
)
grid()
dev.off()

png(file.path(figures_dir, "maximum_regret_by_strategy.png"), width = 1200, height = 800)
barplot(
  regret_summary$maximum_regret,
  names.arg = regret_summary$strategy,
  las = 2,
  main = "Maximum Regret by Strategy",
  ylab = "Maximum regret"
)
grid()
dev.off()

png(file.path(figures_dir, "scenario_score_profiles.png"), width = 1200, height = 800)
plot(
  1,
  type = "n",
  xlim = c(1, length(unique(scenario_results$scenario))),
  ylim = range(scenario_results$composite_score),
  xaxt = "n",
  xlab = "Scenario",
  ylab = "Composite score",
  main = "Scenario Score Profiles"
)

scenario_names <- unique(scenario_results$scenario)
axis(1, at = seq_along(scenario_names), labels = scenario_names, las = 2)

for (strategy_name in unique(scenario_results$strategy)) {
  subset_rows <- scenario_results[scenario_results$strategy == strategy_name, ]
  subset_rows <- subset_rows[match(scenario_names, subset_rows$scenario), ]
  lines(seq_along(scenario_names), subset_rows$composite_score, type = "b")
}

legend("bottomleft", legend = unique(scenario_results$strategy), bty = "n", cex = 0.8)
grid()
dev.off()

print(robustness_summary)
print(regret_summary)
print(head(threshold_rows, 15))
