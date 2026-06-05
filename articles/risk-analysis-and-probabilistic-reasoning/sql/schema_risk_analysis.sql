-- schema_risk_analysis.sql
-- SQLite-compatible schema for risk analysis and probabilistic reasoning.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS model_runs;
DROP TABLE IF EXISTS stress_scenarios;
DROP TABLE IF EXISTS consequences;
DROP TABLE IF EXISTS probabilities;
DROP TABLE IF EXISTS hazards;
DROP TABLE IF EXISTS strategies;

CREATE TABLE strategies (
    strategy_id INTEGER PRIMARY KEY,
    strategy_name TEXT NOT NULL UNIQUE,
    mean_return REAL,
    volatility REAL,
    shock_probability REAL,
    shock_size REAL,
    recovery_credit REAL,
    description TEXT
);

CREATE TABLE hazards (
    hazard_id TEXT PRIMARY KEY,
    hazard_name TEXT NOT NULL,
    category TEXT,
    description TEXT
);

CREATE TABLE probabilities (
    probability_id INTEGER PRIMARY KEY,
    hazard_id TEXT NOT NULL,
    strategy_name TEXT NOT NULL,
    probability REAL NOT NULL CHECK (probability >= 0 AND probability <= 1),
    quality TEXT CHECK (quality IN ('low', 'medium', 'high')),
    source_type TEXT,
    confidence REAL CHECK (confidence >= 0 AND confidence <= 1),
    FOREIGN KEY (hazard_id) REFERENCES hazards(hazard_id),
    FOREIGN KEY (strategy_name) REFERENCES strategies(strategy_name)
);

CREATE TABLE consequences (
    consequence_id INTEGER PRIMARY KEY,
    hazard_id TEXT NOT NULL,
    strategy_name TEXT NOT NULL,
    loss REAL NOT NULL,
    consequence_category TEXT,
    FOREIGN KEY (hazard_id) REFERENCES hazards(hazard_id),
    FOREIGN KEY (strategy_name) REFERENCES strategies(strategy_name)
);

CREATE TABLE stress_scenarios (
    scenario_id INTEGER PRIMARY KEY,
    scenario_name TEXT NOT NULL UNIQUE,
    return_shift REAL,
    volatility_multiplier REAL,
    shock_multiplier REAL,
    description TEXT
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
    selected_strategy TEXT,
    probability_assumptions TEXT,
    consequence_assumptions TEXT,
    stress_test_notes TEXT,
    tail_risk_notes TEXT,
    risk_response TEXT,
    review_trigger TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
