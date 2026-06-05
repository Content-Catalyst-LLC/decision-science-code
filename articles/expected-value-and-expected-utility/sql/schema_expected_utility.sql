-- schema_expected_utility.sql
-- SQLite-compatible schema for expected value and expected utility workflows.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS model_runs;
DROP TABLE IF EXISTS utility_models;
DROP TABLE IF EXISTS probabilities;
DROP TABLE IF EXISTS outcomes;
DROP TABLE IF EXISTS prospects;

CREATE TABLE prospects (
    prospect_id INTEGER PRIMARY KEY,
    prospect_name TEXT NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE outcomes (
    outcome_id INTEGER PRIMARY KEY,
    prospect_id INTEGER NOT NULL,
    outcome_state TEXT NOT NULL,
    outcome_value REAL NOT NULL,
    FOREIGN KEY (prospect_id) REFERENCES prospects(prospect_id)
);

CREATE TABLE probabilities (
    probability_id INTEGER PRIMARY KEY,
    outcome_id INTEGER NOT NULL,
    probability_set TEXT NOT NULL,
    probability REAL NOT NULL CHECK (probability >= 0 AND probability <= 1),
    quality TEXT CHECK (quality IN ('low', 'medium', 'high')),
    source_type TEXT,
    FOREIGN KEY (outcome_id) REFERENCES outcomes(outcome_id)
);

CREATE TABLE utility_models (
    utility_model_id INTEGER PRIMARY KEY,
    model_name TEXT NOT NULL UNIQUE,
    model_family TEXT NOT NULL,
    risk_aversion REAL,
    offset REAL DEFAULT 151.0,
    notes TEXT
);

CREATE TABLE model_runs (
    run_id INTEGER PRIMARY KEY,
    workflow_name TEXT NOT NULL,
    language TEXT NOT NULL,
    run_timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL
);

CREATE TABLE decision_records (
    record_id INTEGER PRIMARY KEY,
    decision_context TEXT NOT NULL,
    selected_prospect TEXT,
    expected_value_summary TEXT,
    expected_utility_summary TEXT,
    probability_assumptions TEXT,
    utility_assumptions TEXT,
    sensitivity_notes TEXT,
    review_trigger TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
