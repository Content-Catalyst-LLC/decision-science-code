-- schema_probability_calibration.sql
-- SQLite-compatible schema for probability calibration and decision confidence.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS model_runs;
DROP TABLE IF EXISTS thresholds;
DROP TABLE IF EXISTS scoring_rules;
DROP TABLE IF EXISTS calibration_bins;
DROP TABLE IF EXISTS outcomes;
DROP TABLE IF EXISTS forecasts;

CREATE TABLE forecasts (
    forecast_id INTEGER PRIMARY KEY,
    domain TEXT NOT NULL,
    event_definition TEXT,
    forecast_probability REAL NOT NULL CHECK (forecast_probability >= 0 AND forecast_probability <= 1),
    reference_class TEXT,
    base_rate REAL CHECK (base_rate >= 0 AND base_rate <= 1),
    confidence_profile TEXT,
    forecast_date TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE outcomes (
    outcome_id INTEGER PRIMARY KEY,
    forecast_id INTEGER NOT NULL,
    outcome INTEGER NOT NULL CHECK (outcome IN (0, 1)),
    resolution_date TEXT,
    resolution_notes TEXT,
    FOREIGN KEY (forecast_id) REFERENCES forecasts(forecast_id)
);

CREATE TABLE calibration_bins (
    bin_id INTEGER PRIMARY KEY,
    bin_lower REAL NOT NULL,
    bin_upper REAL NOT NULL,
    label TEXT NOT NULL
);

CREATE TABLE scoring_rules (
    score_id INTEGER PRIMARY KEY,
    forecast_id INTEGER NOT NULL,
    brier_score REAL,
    log_loss REAL,
    probability_bin TEXT,
    calibration_gap REAL,
    scored_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (forecast_id) REFERENCES forecasts(forecast_id)
);

CREATE TABLE thresholds (
    threshold_id INTEGER PRIMARY KEY,
    decision_context TEXT NOT NULL,
    probability_threshold REAL NOT NULL CHECK (probability_threshold >= 0 AND probability_threshold <= 1),
    false_positive_cost REAL,
    false_negative_cost REAL,
    review_owner TEXT
);

CREATE TABLE model_runs (
    run_id INTEGER PRIMARY KEY,
    workflow_name TEXT NOT NULL,
    language TEXT NOT NULL,
    status TEXT NOT NULL,
    run_timestamp TEXT DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE decision_records (
    record_id INTEGER PRIMARY KEY,
    decision_context TEXT NOT NULL,
    event_definition TEXT,
    forecast_probability REAL,
    probability_range TEXT,
    base_rate REAL,
    reference_class TEXT,
    decision_threshold REAL,
    selected_action TEXT,
    outcome INTEGER,
    calibration_notes TEXT,
    review_trigger TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
