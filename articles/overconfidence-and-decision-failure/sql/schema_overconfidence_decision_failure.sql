-- schema_overconfidence_decision_failure.sql
-- SQLite-compatible schema for overconfidence and decision failure.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS review_triggers;
DROP TABLE IF EXISTS calibration_bins;
DROP TABLE IF EXISTS planning_estimates;
DROP TABLE IF EXISTS confidence_estimates;
DROP TABLE IF EXISTS forecasts;

CREATE TABLE forecasts (
    forecast_id TEXT PRIMARY KEY,
    domain TEXT NOT NULL,
    forecast_probability REAL CHECK (forecast_probability >= 0 AND forecast_probability <= 1),
    confidence REAL CHECK (confidence >= 0 AND confidence <= 1),
    outcome INTEGER CHECK (outcome IN (0, 1)),
    evidence_quality TEXT
);

CREATE TABLE confidence_estimates (
    case_id INTEGER PRIMARY KEY,
    domain TEXT NOT NULL,
    confidence REAL CHECK (confidence >= 0 AND confidence <= 1),
    accuracy_proxy REAL CHECK (accuracy_proxy >= 0 AND accuracy_proxy <= 1),
    confidence_source TEXT
);

CREATE TABLE planning_estimates (
    case_id INTEGER PRIMARY KEY,
    domain TEXT NOT NULL,
    estimated_duration REAL,
    actual_duration REAL,
    estimated_cost REAL,
    actual_cost REAL
);

CREATE TABLE calibration_bins (
    bin_id TEXT PRIMARY KEY,
    probability_bin TEXT NOT NULL,
    average_forecast_probability REAL,
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
    confidence REAL,
    uncertainty_range TEXT,
    selected_action TEXT,
    rationale TEXT,
    review_trigger TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
