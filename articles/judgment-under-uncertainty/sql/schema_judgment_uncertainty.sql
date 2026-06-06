-- schema_judgment_uncertainty.sql
-- SQLite-compatible schema for judgment under uncertainty.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS review_triggers;
DROP TABLE IF EXISTS calibration_bins;
DROP TABLE IF EXISTS forecast_scores;
DROP TABLE IF EXISTS evidence_signals;
DROP TABLE IF EXISTS judgment_cases;

CREATE TABLE judgment_cases (
    case_id INTEGER PRIMARY KEY,
    domain TEXT NOT NULL,
    prior REAL CHECK (prior >= 0 AND prior <= 1),
    likelihood_if_true REAL CHECK (likelihood_if_true >= 0 AND likelihood_if_true <= 1),
    likelihood_if_false REAL CHECK (likelihood_if_false >= 0 AND likelihood_if_false <= 1),
    posterior REAL CHECK (posterior >= 0 AND posterior <= 1),
    anchor REAL CHECK (anchor >= 0 AND anchor <= 1),
    anchor_weight REAL CHECK (anchor_weight >= 0 AND anchor_weight <= 1),
    evidence_quality TEXT
);

CREATE TABLE evidence_signals (
    signal_id TEXT PRIMARY KEY,
    domain TEXT NOT NULL,
    signal_type TEXT,
    reliability REAL,
    diagnostic_strength REAL,
    description TEXT
);

CREATE TABLE forecast_scores (
    forecast_id TEXT PRIMARY KEY,
    case_id INTEGER,
    forecast_probability REAL CHECK (forecast_probability >= 0 AND forecast_probability <= 1),
    confidence REAL CHECK (confidence >= 0 AND confidence <= 1),
    outcome INTEGER CHECK (outcome IN (0, 1)),
    brier_score REAL,
    confidence_gap REAL,
    review_flag TEXT,
    FOREIGN KEY (case_id) REFERENCES judgment_cases(case_id)
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
    prior REAL,
    posterior REAL,
    forecast_probability REAL,
    confidence REAL,
    selected_action TEXT,
    rationale TEXT,
    review_trigger TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
