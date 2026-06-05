# decision_quality_architecture_workflow.R
# Base R workflow for decision quality as a process standard.
# Compares process quality, realized outcomes, robustness, and weight sensitivity.

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

decision_profiles <- read.csv(file.path(article_root, "data", "synthetic_decision_profiles.csv"), stringsAsFactors = FALSE)
weights_table <- read.csv(file.path(article_root, "data", "synthetic_quality_components.csv"), stringsAsFactors = FALSE)

weights <- weights_table$weight
names(weights) <- weights_table$component

if (abs(sum(weights) - 1) > 1e-8) stop("Decision-quality weights must sum to 1.")

components <- names(weights)

decision_profiles$decision_quality_score <- as.numeric(as.matrix(decision_profiles[, components]) %*% weights)
decision_profiles$minimum_component_score <- apply(decision_profiles[, components], 1, min)
decision_profiles$balance_score <- 1 - apply(decision_profiles[, components], 1, sd)

decision_profiles$architecture_score <- (
  0.55 * decision_profiles$decision_quality_score +
  0.25 * decision_profiles$minimum_component_score +
  0.20 * decision_profiles$balance_score
)

decision_profiles$process_profile <- ifelse(
  decision_profiles$architecture_score >= 0.84 & decision_profiles$minimum_component_score >= 0.75,
  "high-quality judgment architecture",
  ifelse(
    decision_profiles$decision_quality_score >= 0.75,
    "solid but uneven decision process",
    "fragile decision process"
  )
)

set.seed(42)

simulation_rows <- data.frame()

for (i in seq_len(nrow(decision_profiles))) {
  profile <- decision_profiles[i, ]

  for (trial in 1:1000) {
    shock <- rnorm(1, mean = 0, sd = 22)
    implementation_noise <- rnorm(1, mean = 0, sd = 8)

    realized_outcome <- (
      profile$expected_value -
      45 * profile$downside_exposure * max(0, rnorm(1, mean = 0.45, sd = 0.30)) +
      18 * profile$learning_design +
      14 * profile$accountability +
      10 * profile$behavioral_safeguards +
      shock +
      implementation_noise
    )

    simulation_rows <- rbind(
      simulation_rows,
      data.frame(
        trial = trial,
        alternative = profile$alternative,
        decision_quality_score = profile$decision_quality_score,
        architecture_score = profile$architecture_score,
        realized_outcome = realized_outcome,
        favorable_outcome = realized_outcome >= 75,
        process_profile = profile$process_profile,
        stringsAsFactors = FALSE
      )
    )
  }
}

outcome_summary <- aggregate(
  realized_outcome ~ alternative,
  data = simulation_rows,
  FUN = function(x) c(mean = mean(x), min = min(x), max = max(x), sd = sd(x))
)

outcome_summary_expanded <- data.frame(
  alternative = outcome_summary$alternative,
  mean_outcome = outcome_summary$realized_outcome[, "mean"],
  minimum_outcome = outcome_summary$realized_outcome[, "min"],
  maximum_outcome = outcome_summary$realized_outcome[, "max"],
  outcome_sd = outcome_summary$realized_outcome[, "sd"]
)

favorable_summary <- aggregate(favorable_outcome ~ alternative, data = simulation_rows, FUN = mean)
names(favorable_summary) <- c("alternative", "favorable_outcome_rate")

diagnostic_report <- merge(decision_profiles, outcome_summary_expanded, by = "alternative")
diagnostic_report <- merge(diagnostic_report, favorable_summary, by = "alternative")

diagnostic_report$outcome_bias_warning <- ifelse(
  diagnostic_report$decision_quality_score < 0.60 & diagnostic_report$favorable_outcome_rate > 0.50,
  "possible luck masking weak process",
  ifelse(
    diagnostic_report$decision_quality_score >= 0.80 & diagnostic_report$favorable_outcome_rate < 0.50,
    "sound process exposed to unfavorable uncertainty",
    "process and outcome broadly aligned"
  )
)

diagnostic_report <- diagnostic_report[order(-diagnostic_report$architecture_score), ]

write.csv(decision_profiles, file.path(tables_dir, "decision_quality_profiles.csv"), row.names = FALSE)
write.csv(simulation_rows, file.path(tables_dir, "decision_quality_outcome_simulation.csv"), row.names = FALSE)
write.csv(diagnostic_report, file.path(tables_dir, "decision_quality_diagnostic_report.csv"), row.names = FALSE)

sensitivity_rows <- data.frame()

for (component in components) {
  for (delta in c(-0.05, 0.05)) {
    revised_weights <- weights
    revised_weights[component] <- max(0.01, revised_weights[component] + delta)
    revised_weights <- revised_weights / sum(revised_weights)

    revised_score <- as.numeric(as.matrix(decision_profiles[, components]) %*% revised_weights)

    temp <- data.frame(
      changed_component = component,
      delta = delta,
      alternative = decision_profiles$alternative,
      revised_decision_quality_score = revised_score,
      stringsAsFactors = FALSE
    )

    temp$top_alternative_after_change <- temp$alternative[which.max(temp$revised_decision_quality_score)]
    sensitivity_rows <- rbind(sensitivity_rows, temp)
  }
}

write.csv(sensitivity_rows, file.path(tables_dir, "decision_quality_weight_sensitivity.csv"), row.names = FALSE)

png(file.path(figures_dir, "decision_quality_score_by_alternative.png"), width = 1200, height = 800)
barplot(diagnostic_report$decision_quality_score, names.arg = diagnostic_report$alternative, las = 2, main = "Decision Quality Score by Alternative", ylab = "Decision quality score")
grid()
dev.off()

png(file.path(figures_dir, "architecture_score_by_alternative.png"), width = 1200, height = 800)
barplot(diagnostic_report$architecture_score, names.arg = diagnostic_report$alternative, las = 2, main = "Architecture of Judgment Score by Alternative", ylab = "Architecture score")
grid()
dev.off()

png(file.path(figures_dir, "favorable_outcome_rate_by_alternative.png"), width = 1200, height = 800)
barplot(diagnostic_report$favorable_outcome_rate, names.arg = diagnostic_report$alternative, las = 2, main = "Favorable Outcome Rate by Alternative", ylab = "Favorable outcome rate")
grid()
dev.off()

print(diagnostic_report)
