# decision_records_accountable_judgment_workflow.R
# Base R workflow for evaluating decision record quality:
# completeness, traceability, assumption criticality, review triggers,
# dissent preservation, and accountability readiness.

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

records <- read.csv(file.path(article_root, "data", "synthetic_decision_records.csv"), stringsAsFactors = FALSE, check.names = FALSE)
components_table <- read.csv(file.path(article_root, "data", "synthetic_record_components.csv"), stringsAsFactors = FALSE)
claims <- read.csv(file.path(article_root, "data", "synthetic_claims.csv"), stringsAsFactors = FALSE)
assumptions <- read.csv(file.path(article_root, "data", "synthetic_assumptions.csv"), stringsAsFactors = FALSE)
triggers <- read.csv(file.path(article_root, "data", "synthetic_review_triggers.csv"), stringsAsFactors = FALSE)

weights <- components_table$weight
names(weights) <- components_table$component

if (abs(sum(weights) - 1) > 1e-8) stop("Weights must sum to 1.")

components <- names(weights)

records$decision_record_quality <- as.numeric(as.matrix(records[, components]) %*% weights)
records$minimum_component_score <- apply(records[, components], 1, min)
records$record_balance <- 1 - apply(records[, components], 1, sd)

records$accountable_judgment_score <- (
  0.55 * records$decision_record_quality +
  0.25 * records$minimum_component_score +
  0.20 * records$record_balance
)

records$quality_profile <- ifelse(
  records$accountable_judgment_score >= 0.84 & records$minimum_component_score >= 0.70,
  "strong accountable judgment record",
  ifelse(records$decision_record_quality >= 0.72, "usable record with improvement needs", "fragile or incomplete decision record")
)

claims$evidence_linked_logical <- tolower(as.character(claims$evidence_linked)) %in% c("true", "1", "yes", "y")

traceability_summary <- aggregate(evidence_linked_logical ~ record_id, data = claims, FUN = mean)
names(traceability_summary) <- c("record_id", "traceability_share")

evidence_summary <- aggregate(evidence_quality ~ record_id, data = claims, FUN = mean)
names(evidence_summary) <- c("record_id", "claim_evidence_quality")

records <- merge(records, traceability_summary, by = "record_id", all.x = TRUE)
records <- merge(records, evidence_summary, by = "record_id", all.x = TRUE)

records$traceability_share[is.na(records$traceability_share)] <- 0
records$claim_evidence_quality[is.na(records$claim_evidence_quality)] <- 0

assumptions$monitored_logical <- tolower(as.character(assumptions$monitored)) %in% c("true", "1", "yes", "y")
assumptions$assumption_risk <- assumptions$criticality * (1 - assumptions$confidence)
assumptions$monitoring_gap <- assumptions$criticality >= 0.75 & !assumptions$monitored_logical

assumption_summary <- aggregate(assumption_risk ~ record_id, data = assumptions, FUN = mean)
monitoring_gap_summary <- aggregate(monitoring_gap ~ record_id, data = assumptions, FUN = function(x) sum(x))

names(monitoring_gap_summary) <- c("record_id", "critical_monitoring_gaps")

records <- merge(records, assumption_summary, by = "record_id", all.x = TRUE)
records <- merge(records, monitoring_gap_summary, by = "record_id", all.x = TRUE)

records$assumption_risk[is.na(records$assumption_risk)] <- 0
records$critical_monitoring_gaps[is.na(records$critical_monitoring_gaps)] <- 0

triggers$active_review_trigger <- triggers$current_value < triggers$lower_bound | triggers$current_value > triggers$upper_bound
trigger_summary <- aggregate(active_review_trigger ~ record_id, data = triggers, FUN = function(x) sum(x))
names(trigger_summary) <- c("record_id", "active_review_triggers")

records <- merge(records, trigger_summary, by = "record_id", all.x = TRUE)
records$active_review_triggers[is.na(records$active_review_triggers)] <- 0

records$review_priority_score <- (
  0.35 * (1 - records$accountable_judgment_score) +
  0.20 * records$assumption_risk +
  0.20 * (1 - records$traceability_share) +
  0.15 * pmin(records$critical_monitoring_gaps, 3) / 3 +
  0.10 * pmin(records$active_review_triggers, 3) / 3
)

records$review_priority <- ifelse(
  records$review_priority_score >= 0.45,
  "high",
  ifelse(records$review_priority_score >= 0.25, "medium", "low")
)

records <- records[order(-records$accountable_judgment_score), ]

write.csv(records, file.path(tables_dir, "decision_record_quality_summary.csv"), row.names = FALSE)
write.csv(claims, file.path(tables_dir, "decision_record_claim_traceability.csv"), row.names = FALSE)
write.csv(assumptions, file.path(tables_dir, "decision_record_assumption_audit.csv"), row.names = FALSE)
write.csv(triggers, file.path(tables_dir, "decision_record_review_triggers.csv"), row.names = FALSE)

png(file.path(figures_dir, "decision_record_quality_scores.png"), width = 1200, height = 800)
barplot(records$accountable_judgment_score, names.arg = records$record_id, las = 2, main = "Accountable Judgment Score by Decision Record", ylab = "Accountable judgment score")
grid()
dev.off()

png(file.path(figures_dir, "decision_record_review_priority.png"), width = 1200, height = 800)
barplot(records$review_priority_score, names.arg = records$record_id, las = 2, main = "Review Priority Score by Decision Record", ylab = "Review priority score")
grid()
dev.off()

print(records)
