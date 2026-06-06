# framing_effects_decision_making_workflow.R
# Base R workflow for gain-loss framing, reference points,
# prospect-style valuation, frame reversals, and decision-review tables.

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

n <- 800

domains <- c(
  "Healthcare",
  "Public Policy",
  "Financial Risk",
  "Infrastructure",
  "AI Governance",
  "Organizational Strategy"
)

cases <- data.frame(
  case_id = seq_len(n),
  domain = sample(domains, n, replace = TRUE),
  reference_point = sample(c(-100, 0, 100), n, replace = TRUE, prob = c(0.25, 0.50, 0.25)),
  sure_outcome = sample(c(80, 120, 160, 200), n, replace = TRUE),
  risky_high_outcome = sample(c(180, 240, 300, 360), n, replace = TRUE),
  risky_high_probability = runif(n, 0.45, 0.85),
  loss_aversion = runif(n, 1.4, 2.8),
  alpha = runif(n, 0.75, 0.95),
  beta = runif(n, 0.75, 0.95),
  stringsAsFactors = FALSE
)

cases$risky_low_outcome <- 0
cases$risky_low_probability <- 1 - cases$risky_high_probability

prospect_value <- function(x, alpha, beta, lambda) {
  ifelse(x >= 0, x^alpha, -lambda * ((-x)^beta))
}

expected_value <- function(high, phigh, low, plow) {
  high * phigh + low * plow
}

prospect_score <- function(high, phigh, low, plow, reference, alpha, beta, lambda) {
  phigh * prospect_value(high - reference, alpha, beta, lambda) +
    plow * prospect_value(low - reference, alpha, beta, lambda)
}

cases$sure_gain <- cases$sure_outcome
cases$risky_gain_high <- cases$risky_high_outcome
cases$risky_gain_low <- cases$risky_low_outcome

cases$sure_loss <- -cases$sure_outcome
cases$risky_loss_high <- -cases$risky_high_outcome
cases$risky_loss_low <- cases$risky_low_outcome

cases$ev_sure_gain <- cases$sure_gain
cases$ev_risky_gain <- expected_value(
  cases$risky_gain_high,
  cases$risky_high_probability,
  cases$risky_gain_low,
  cases$risky_low_probability
)

cases$ev_sure_loss <- cases$sure_loss
cases$ev_risky_loss <- expected_value(
  cases$risky_loss_high,
  cases$risky_high_probability,
  cases$risky_loss_low,
  cases$risky_low_probability
)

cases$prospect_sure_gain <- prospect_score(
  cases$sure_gain, 1, 0, 0,
  cases$reference_point, cases$alpha, cases$beta, cases$loss_aversion
)

cases$prospect_risky_gain <- prospect_score(
  cases$risky_gain_high,
  cases$risky_high_probability,
  cases$risky_gain_low,
  cases$risky_low_probability,
  cases$reference_point,
  cases$alpha,
  cases$beta,
  cases$loss_aversion
)

cases$prospect_sure_loss <- prospect_score(
  cases$sure_loss, 1, 0, 0,
  cases$reference_point, cases$alpha, cases$beta, cases$loss_aversion
)

cases$prospect_risky_loss <- prospect_score(
  cases$risky_loss_high,
  cases$risky_high_probability,
  cases$risky_loss_low,
  cases$risky_low_probability,
  cases$reference_point,
  cases$alpha,
  cases$beta,
  cases$loss_aversion
)

cases$gain_frame_choice <- ifelse(
  cases$prospect_sure_gain >= cases$prospect_risky_gain,
  "sure option",
  "risky option"
)

cases$loss_frame_choice <- ifelse(
  cases$prospect_sure_loss >= cases$prospect_risky_loss,
  "sure option",
  "risky option"
)

cases$frame_reversal <- cases$gain_frame_choice != cases$loss_frame_choice
cases$gain_frame_risk_premium <- cases$prospect_risky_gain - cases$prospect_sure_gain
cases$loss_frame_risk_premium <- cases$prospect_risky_loss - cases$prospect_sure_loss
cases$frame_sensitivity_index <- abs(cases$gain_frame_risk_premium - cases$loss_frame_risk_premium)

sensitivity_threshold <- as.numeric(quantile(cases$frame_sensitivity_index, 0.80))

cases$review_flag <- ifelse(
  cases$frame_reversal | cases$frame_sensitivity_index >= sensitivity_threshold,
  "review",
  "acceptable"
)

write.csv(
  cases,
  file.path(tables_dir, "framing_effects_choice_cases.csv"),
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
        frame_reversal_rate = mean(x$frame_reversal),
        average_frame_sensitivity_index = mean(x$frame_sensitivity_index),
        gain_risky_choice_rate = mean(x$gain_frame_choice == "risky option"),
        loss_risky_choice_rate = mean(x$loss_frame_choice == "risky option"),
        review_rate = mean(x$review_flag == "review"),
        stringsAsFactors = FALSE
      )
    }
  )
)

domain_summary <- domain_summary[order(-domain_summary$frame_reversal_rate), ]

write.csv(
  domain_summary,
  file.path(tables_dir, "domain_framing_diagnostics.csv"),
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
        frame_reversal_rate = mean(x$frame_reversal),
        average_frame_sensitivity_index = mean(x$frame_sensitivity_index),
        gain_risky_choice_rate = mean(x$gain_frame_choice == "risky option"),
        loss_risky_choice_rate = mean(x$loss_frame_choice == "risky option"),
        stringsAsFactors = FALSE
      )
    }
  )
)

reference_summary <- reference_summary[order(reference_summary$reference_point), ]

write.csv(
  reference_summary,
  file.path(tables_dir, "reference_point_sensitivity_summary.csv"),
  row.names = FALSE
)

attribute_frames <- read.csv(file.path(article_root, "data", "synthetic_attribute_frames.csv"), stringsAsFactors = FALSE)
attribute_frames$equivalence_gap <- abs((1 - attribute_frames$positive_value) - attribute_frames$negative_value)
attribute_frames$review_flag <- ifelse(attribute_frames$equivalence_gap > 0.0001, "review", "equivalent_pair")

write.csv(
  attribute_frames,
  file.path(tables_dir, "attribute_frame_equivalence_checks.csv"),
  row.names = FALSE
)

risk_formats <- read.csv(file.path(article_root, "data", "synthetic_risk_communication_formats.csv"), stringsAsFactors = FALSE)
risk_formats$computed_absolute_change <- risk_formats$new_risk - risk_formats$baseline_risk
risk_formats$computed_relative_change <- risk_formats$computed_absolute_change / risk_formats$baseline_risk
risk_formats$format_warning <- ifelse(abs(risk_formats$computed_relative_change) > 0.25, "show_absolute_and_relative", "standard_display")

write.csv(
  risk_formats,
  file.path(tables_dir, "risk_communication_format_summary.csv"),
  row.names = FALSE
)

review_queue <- cases[cases$review_flag == "review", c(
  "case_id",
  "domain",
  "reference_point",
  "loss_aversion",
  "gain_frame_choice",
  "loss_frame_choice",
  "frame_reversal",
  "frame_sensitivity_index",
  "review_flag"
)]

write.csv(
  review_queue,
  file.path(tables_dir, "framing_review_queue.csv"),
  row.names = FALSE
)

overall_metrics <- data.frame(
  metric = c(
    "frame_reversal_rate",
    "average_frame_sensitivity_index",
    "gain_risky_choice_rate",
    "loss_risky_choice_rate",
    "review_rate"
  ),
  value = c(
    mean(cases$frame_reversal),
    mean(cases$frame_sensitivity_index),
    mean(cases$gain_frame_choice == "risky option"),
    mean(cases$loss_frame_choice == "risky option"),
    mean(cases$review_flag == "review")
  ),
  stringsAsFactors = FALSE
)

write.csv(
  overall_metrics,
  file.path(tables_dir, "overall_framing_effects_metrics.csv"),
  row.names = FALSE
)

png(file.path(figures_dir, "frame_reversal_rate_by_domain.png"), width = 1200, height = 800)
barplot(
  domain_summary$frame_reversal_rate,
  names.arg = domain_summary$domain,
  las = 2,
  main = "Frame Reversal Rate by Domain",
  ylab = "Share of cases with different gain/loss choices"
)
grid()
dev.off()

png(file.path(figures_dir, "reference_point_sensitivity.png"), width = 1200, height = 800)
plot(
  reference_summary$reference_point,
  reference_summary$average_frame_sensitivity_index,
  type = "b",
  xlab = "Reference point",
  ylab = "Average frame sensitivity index",
  main = "Reference Point Sensitivity"
)
grid()
dev.off()

png(file.path(figures_dir, "gain_vs_loss_risky_choice_rates.png"), width = 1200, height = 800)
barplot(
  rbind(
    domain_summary$gain_risky_choice_rate,
    domain_summary$loss_risky_choice_rate
  ),
  beside = TRUE,
  names.arg = domain_summary$domain,
  las = 2,
  main = "Risky Choice Rates Under Gain and Loss Frames",
  ylab = "Risky choice rate"
)
legend(
  "topright",
  legend = c("Gain frame", "Loss frame"),
  fill = gray.colors(2)
)
grid()
dev.off()

print(overall_metrics)
print(domain_summary)
print(reference_summary)
