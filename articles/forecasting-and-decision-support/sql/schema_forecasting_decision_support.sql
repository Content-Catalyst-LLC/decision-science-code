-- schema_forecasting_decision_support.sql
-- SQLite-compatible schema for forecasting and decision support.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS model_runs;
DROP TABLE IF EXISTS forecast_scores;
DROP TABLE IF EXISTS thresholds;
DROP TABLE IF EXISTS reference_classes;
DROP TABLE IF EXISTS outcomes;
DROP TABLE IF EXISTS forecasts;

CREATE TABLE forecasts (
    forecast_id INTEGER PRIMARY KEY,
    domain TEXT NOT NULL,
    forecast_target TEXT,
    base_rate REAL CHECK (base_rate >= 0 AND base_rate <= 1),
    forecast_probability REAL NOT NULL CHECK (forecast_probability >= 0 AND forecast_probability <= 1),
    forecast_horizon_days INTEGER,
    forecast_cost REAL,
    method_notes TEXT,
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

CREATE TABLE reference_classes (
    reference_class_id INTEGER PRIMARY KEY,
    domain TEXT NOT NULL UNIQUE,
    base_rate REAL CHECK (base_rate >= 0 AND base_rate <= 1),
    n_cases INTEGER,
    evidence_quality TEXT CHECK (evidence_quality IN ('low', 'medium', 'high')),
    description TEXT
);

CREATE TABLE thresholds (
    threshold_id INTEGER PRIMARY KEY,
    domain TEXT NOT NULL,
    decision_context TEXT NOT NULL,
    probability_threshold REAL NOT NULL CHECK (probability_threshold >= 0 AND probability_threshold <= 1),
    false_positive_cost REAL,
    false_negative_cost REAL,
    review_owner TEXT
);

CREATE TABLE forecast_scores (
    score_id INTEGER PRIMARY KEY,
    forecast_id INTEGER NOT NULL,
    brier_score REAL,
    log_loss REAL,
    probability_bin TEXT,
    expected_loss_with_forecast REAL,
    expected_loss_without_forecast REAL,
    forecast_value_proxy REAL,
    scored_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (forecast_id) REFERENCES forecasts(forecast_id)
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
    forecast_target TEXT,
    time_horizon TEXT,
    base_rate REAL,
    reference_class TEXT,
    forecast_probability REAL,
    decision_threshold REAL,
    selected_action TEXT,
    expected_loss_with_forecast REAL,
    expected_loss_without_forecast REAL,
    forecast_value_proxy REAL,
    review_trigger TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
