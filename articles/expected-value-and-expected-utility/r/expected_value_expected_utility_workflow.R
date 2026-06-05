# expected_value_expected_utility_workflow.R
# Base R workflow for comparing uncertain prospects using:
# expected value, expected utility, certainty equivalents,
# risk premiums, and risk-aversion sensitivity.

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

outcomes <- read.csv(file.path(article_root, "data", "synthetic_outcomes.csv"), stringsAsFactors = FALSE)
risk_levels <- read.csv(file.path(article_root, "data", "synthetic_risk_aversion_levels.csv"), stringsAsFactors = FALSE)

prob_check <- aggregate(probability ~ prospect, data = outcomes, FUN = sum)
if (any(abs(prob_check$probability - 1) > 1e-8)) {
  stop("Probabilities must sum to 1 for each prospect.")
}

crra_utility <- function(x, rho, offset = 151) {
  z <- x + offset
  if (any(z <= 0)) stop("Shifted outcomes must be positive.")
  if (abs(rho - 1) < 1e-8) {
    return(log(z))
  }
  (z^(1 - rho) - 1) / (1 - rho)
}

inverse_crra <- function(u, rho, offset = 151) {
  if (abs(rho - 1) < 1e-8) {
    return(exp(u) - offset)
  }
  ((u * (1 - rho) + 1)^(1 / (1 - rho))) - offset
}

expected_values <- aggregate(
  outcome * probability ~ prospect,
  data = outcomes,
  FUN = sum
)

names(expected_values) <- c("prospect", "expected_value")

sensitivity_rows <- data.frame()

for (rho in risk_levels$risk_aversion) {
  temp <- outcomes
  temp$utility <- crra_utility(temp$outcome, rho)
  temp$weighted_utility <- temp$probability * temp$utility

  utility_summary <- aggregate(weighted_utility ~ prospect, data = temp, FUN = sum)
  names(utility_summary) <- c("prospect", "expected_utility")

  utility_summary <- merge(utility_summary, expected_values, by = "prospect")
  utility_summary$risk_aversion <- rho
  utility_summary$certainty_equivalent <- inverse_crra(utility_summary$expected_utility, rho)
  utility_summary$risk_premium <- utility_summary$expected_value - utility_summary$certainty_equivalent

  utility_summary$expected_value_rank <- rank(-utility_summary$expected_value, ties.method = "min")
  utility_summary$expected_utility_rank <- rank(-utility_summary$expected_utility, ties.method = "min")
  utility_summary$certainty_equivalent_rank <- rank(-utility_summary$certainty_equivalent, ties.method = "min")

  sensitivity_rows <- rbind(sensitivity_rows, utility_summary)
}

ranking_instability <- aggregate(
  expected_utility_rank ~ prospect,
  data = sensitivity_rows,
  FUN = function(x) max(x) - min(x)
)

names(ranking_instability) <- c("prospect", "expected_utility_rank_range")

risk_premium_summary <- aggregate(
  risk_premium ~ prospect,
  data = sensitivity_rows,
  FUN = mean
)

names(risk_premium_summary) <- c("prospect", "average_risk_premium")

summary_table <- merge(expected_values, ranking_instability, by = "prospect")
summary_table <- merge(summary_table, risk_premium_summary, by = "prospect")
summary_table <- summary_table[order(-summary_table$expected_value), ]

write.csv(expected_values, file.path(tables_dir, "expected_value_profiles.csv"), row.names = FALSE)
write.csv(sensitivity_rows, file.path(tables_dir, "risk_aversion_sensitivity.csv"), row.names = FALSE)
write.csv(summary_table, file.path(tables_dir, "expected_utility_summary_table.csv"), row.names = FALSE)

png(file.path(figures_dir, "expected_value_by_prospect.png"), width = 1200, height = 800)
barplot(
  expected_values$expected_value,
  names.arg = expected_values$prospect,
  las = 2,
  main = "Expected Value by Prospect",
  ylab = "Expected value"
)
grid()
dev.off()

log_rows <- sensitivity_rows[sensitivity_rows$risk_aversion == 1.0, ]

png(file.path(figures_dir, "risk_premium_log_utility.png"), width = 1200, height = 800)
barplot(
  log_rows$risk_premium,
  names.arg = log_rows$prospect,
  las = 2,
  main = "Risk Premium Under Log Utility",
  ylab = "Risk premium"
)
grid()
dev.off()

png(file.path(figures_dir, "certainty_equivalent_by_risk_aversion.png"), width = 1200, height = 800)
plot(
  sensitivity_rows$risk_aversion,
  sensitivity_rows$certainty_equivalent,
  type = "n",
  xlab = "Risk aversion",
  ylab = "Certainty equivalent",
  main = "Certainty Equivalent Across Risk Aversion"
)

for (prospect_name in unique(sensitivity_rows$prospect)) {
  subset_rows <- sensitivity_rows[sensitivity_rows$prospect == prospect_name, ]
  lines(subset_rows$risk_aversion, subset_rows$certainty_equivalent, type = "b")
}

legend("topright", legend = unique(sensitivity_rows$prospect), bty = "n", cex = 0.8)
grid()
dev.off()

print(summary_table)
