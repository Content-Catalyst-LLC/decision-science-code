-- schema_decision_hygiene_bias_reduction.sql
-- SQLite-compatible schema for decision hygiene and bias reduction.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS review_triggers;
DROP TABLE IF EXISTS calibration_bins;
DROP TABLE IF EXISTS hygiene_practices;
DROP TABLE IF EXISTS bias_sources;
DROP TABLE IF EXISTS decision_cases;

CREATE TABLE decision_cases (
    case_id INTEGER PRIMARY KEY,
    domain TEXT NOT NULL,
    bias_source TEXT,
    hygiene_practice TEXT,
    true_value REAL,
    evidence_quality TEXT,
    decision_stakes TEXT,
    pre_hygiene_judgment REAL,
    post_hygiene_judgment REAL,
    outcome INTEGER
);

CREATE TABLE bias_sources (
    bias_source TEXT PRIMARY KEY,
    description TEXT,
    primary_hygiene_response TEXT
);

CREATE TABLE hygiene_practices (
    hygiene_practice TEXT PRIMARY KEY,
    description TEXT,
    target_failure_mode TEXT
);

CREATE TABLE calibration_bins (
    bin_id TEXT PRIMARY KEY,
    probability_bin TEXT NOT NULL,
    average_probability REAL,
    observed_frequency REAL,
    n_cases INTEGER,
    calibration_gap REAL
);

CREATE TABLE review_triggers (
    trigger_id TEXT PRIMARY KEY,
    indicator TEXT NOT NULL,
    threshold_direction TEXT NOT NULL,
    threshold_value REAL,
    review_owner TEXT
);

CREATE TABLE decision_records (
    record_id TEXT PRIMARY KEY,
    decision_context TEXT NOT NULL,
    hygiene_practice TEXT,
    selected_action TEXT,
    rationale TEXT,
    review_trigger TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
