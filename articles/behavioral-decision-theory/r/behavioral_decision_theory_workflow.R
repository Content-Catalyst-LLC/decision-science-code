# behavioral_decision_theory_workflow.R
# Base R workflow for expected utility, prospect-theory scoring,
# probability weighting, reference dependence, and behavioral diagnostics.

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

domains <- c(
  "Public Policy",
  "Healthcare",
  "Financial Risk",
  "Infrastructure",
  "AI Governance",
  "Organizational Strategy"
)

n <- 720

cases <- data.frame(
  case_id = seq_len(n),
  domain = sample(domains, n, replace = TRUE),
  option_name = sample(
    c("Status Quo", "Cautious Alternative", "Balanced Alternative", "High-Upside Alternative", "Loss-Avoidance Alternative"),
    n,
    replace = TRUE
  ),
  reference_point = sample(c(-100, 0, 100), n, replace = TRUE, prob = c(0.25, 0.50, 0.25)),
  outcome_high = sample(c(80, 120, 180, 240, 320), n, replace = TRUE),
  probability_high = runif(n, 0.10, 0.90),
  outcome_low = sample(c(-160, -80, 0, 40), n, replace = TRUE),
  loss_aversion = runif(n, 1.4, 3.0),
  alpha = runif(n, 0.75, 0.95),
  beta = runif(n, 0.75, 0.95),
  gamma = runif(n, 0.55, 0.95),
  stringsAsFactors = FALSE
)

cases$probability_low <- 1 - cases$probability_high

utility <- function(x) {
  sign(x) * sqrt(abs(x))
}

prospect_value <- function(x, alpha, beta, lambda) {
  ifelse(x >= 0, x^alpha, -lambda * ((-x)^beta))
}

weighted_probability <- function(p, gamma) {
  numerator <- p^gamma
  denominator <- (p^gamma + (1 - p)^gamma)^(1 / gamma)
  numerator / denominator
}

cases$expected_value <- cases$outcome_high * cases$probability_high +
  cases$outcome_low * cases$probability_low

cases$expected_utility <- cases$probability_high * utility(cases$outcome_high) +
  cases$probability_low * utility(cases$outcome_low)

cases$weighted_high <- weighted_probability(cases$probability_high, cases$gamma)
cases$weighted_low <- weighted_probability(cases$probability_low, cases$gamma)

cases$prospect_score <- cases$weighted_high *
  prospect_value(cases$outcome_high - cases$reference_point, cases$alpha, cases$beta, cases$loss_aversion) +
  cases$weighted_low *
  prospect_value(cases$outcome_low - cases$reference_point, cases$alpha, cases$beta, cases$loss_aversion)

cases$gain_frame_score <- cases$weighted_high *
  prospect_value(abs(cases$outcome_high), cases$alpha, cases$beta, cases$loss_aversion) +
  cases$weighted_low *
  prospect_value(abs(cases$outcome_low), cases$alpha, cases$beta, cases$loss_aversion)

cases$loss_frame_score <- cases$weighted_high *
  prospect_value(-abs(cases$outcome_high), cases$alpha, cases$beta, cases$loss_aversion) +
  cases$weighted_low *
  prospect_value(-abs(cases$outcome_low), cases$alpha, cases$beta, cases$loss_aversion)

cases$frame_sensitivity_index <- abs(cases$gain_frame_score - cases$loss_frame_score)
cases$probability_weight_distortion <- abs(cases$weighted_high - cases$probability_high)

cases$eu_rank <- ave(
  -cases$expected_utility,
  cases$domain,
  FUN = function(x) rank(x, ties.method = "average")
)

cases$prospect_rank <- ave(
  -cases$prospect_score,
  cases$domain,
  FUN = function(x) rank(x, ties.method = "average")
)

cases$rank_divergence <- cases$eu_rank - cases$prospect_rank

cases$review_flag <- ifelse(
  abs(cases$rank_divergence) > quantile(abs(cases$rank_divergence), 0.80) |
    cases$frame_sensitivity_index > quantile(cases$frame_sensitivity_index, 0.80) |
    cases$probability_weight_distortion > quantile(cases$probability_weight_distortion, 0.80) |
    cases$loss_aversion >= 2.5,
  "review",
  "acceptable"
)

write.csv(
  cases,
  file.path(tables_dir, "behavioral_decision_theory_cases.csv"),
  row.names = FALSE
)

domain_summary <- do.call(
  rbind,
  lapply(
    split(cases, cases$domain),
    function(x) {
      data.frame(
        domain = unique(x$domain),
        n_cases = nrow(x),
        average_expected_value = mean(x$expected_value),
        average_expected_utility = mean(x$expected_utility),
        average_prospect_score = mean(x$prospect_score),
        average_probability_weight_distortion = mean(x$probability_weight_distortion),
        average_frame_sensitivity_index = mean(x$frame_sensitivity_index),
        average_absolute_rank_divergence = mean(abs(x$rank_divergence)),
        review_rate = mean(x$review_flag == "review"),
        stringsAsFactors = FALSE
      )
    }
  )
)

domain_summary <- domain_summary[order(-domain_summary$review_rate), ]

write.csv(
  domain_summary,
  file.path(tables_dir, "domain_behavioral_decision_summary.csv"),
  row.names = FALSE
)

reference_summary <- do.call(
  rbind,
  lapply(
    split(cases, cases$reference_point),
    function(x) {
      data.frame(
        reference_point = unique(x$reference_point),
        n_cases = nrow(x),
        average_prospect_score = mean(x$prospect_score),
        average_frame_sensitivity_index = mean(x$frame_sensitivity_index),
        average_absolute_rank_divergence = mean(abs(x$rank_divergence)),
        review_rate = mean(x$review_flag == "review"),
        stringsAsFactors = FALSE
      )
    }
  )
)

reference_summary <- reference_summary[order(reference_summary$reference_point), ]

write.csv(
  reference_summary,
  file.path(tables_dir, "reference_point_behavioral_summary.csv"),
  row.names = FALSE
)

review_queue <- cases[cases$review_flag == "review", c(
  "case_id",
  "domain",
  "option_name",
  "reference_point",
  "expected_value",
  "expected_utility",
  "prospect_score",
  "probability_weight_distortion",
  "frame_sensitivity_index",
  "rank_divergence",
  "loss_aversion",
  "review_flag"
)]

write.csv(
  review_queue,
  file.path(tables_dir, "behavioral_decision_review_queue.csv"),
  row.names = FALSE
)

overall_metrics <- data.frame(
  metric = c(
    "mean_expected_value",
    "mean_expected_utility",
    "mean_prospect_score",
    "mean_probability_weight_distortion",
    "mean_frame_sensitivity_index",
    "mean_absolute_rank_divergence",
    "review_rate"
  ),
  value = c(
    mean(cases$expected_value),
    mean(cases$expected_utility),
    mean(cases$prospect_score),
    mean(cases$probability_weight_distortion),
    mean(cases$frame_sensitivity_index),
    mean(abs(cases$rank_divergence)),
    mean(cases$review_flag == "review")
  ),
  stringsAsFactors = FALSE
)

write.csv(
  overall_metrics,
  file.path(tables_dir, "overall_behavioral_decision_metrics.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "behavioral_review_rate_by_domain.png"), width = 1200, height = 800)
barplot(
  domain_summary$review_rate,
  names.arg = domain_summary$domain,
  las = 2,
  main = "Behavioral Review Rate by Domain",
  ylab = "Review rate"
)
grid()
dev.off()

png(file.path(figures_dir, "probability_weight_distortion_by_domain.png"), width = 1200, height = 800)
barplot(
  domain_summary$average_probability_weight_distortion,
  names.arg = domain_summary$domain,
  las = 2,
  main = "Probability Weight Distortion by Domain",
  ylab = "Average absolute distortion"
)
grid()
dev.off()

png(file.path(figures_dir, "frame_sensitivity_by_reference_point.png"), width = 1200, height = 800)
plot(
  reference_summary$reference_point,
  reference_summary$average_frame_sensitivity_index,
  type = "b",
  xlab = "Reference point",
  ylab = "Average frame sensitivity index",
  main = "Frame Sensitivity by Reference Point"
)
grid()
dev.off()

print(overall_metrics)
print(domain_summary)
print(reference_summary)
