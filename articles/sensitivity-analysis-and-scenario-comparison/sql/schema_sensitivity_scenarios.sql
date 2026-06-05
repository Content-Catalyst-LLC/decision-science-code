-- schema_sensitivity_scenarios.sql
-- SQLite-compatible schema for sensitivity analysis and scenario comparison.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS model_runs;
DROP TABLE IF EXISTS thresholds;
DROP TABLE IF EXISTS scenario_scores;
DROP TABLE IF EXISTS scenarios;
DROP TABLE IF EXISTS parameters;
DROP TABLE IF EXISTS strategies;

CREATE TABLE strategies (
    strategy_id INTEGER PRIMARY KEY,
    strategy_name TEXT NOT NULL UNIQUE,
    base_value REAL,
    demand_sensitivity REAL,
    cost_sensitivity REAL,
    disruption_sensitivity REAL,
    resilience_buffer REAL,
    adaptation_capacity REAL,
    description TEXT
);

CREATE TABLE parameters (
    parameter_id INTEGER PRIMARY KEY,
    parameter_name TEXT NOT NULL UNIQUE,
    baseline REAL,
    low_value REAL,
    high_value REAL,
    evidence_quality TEXT CHECK (evidence_quality IN ('low', 'medium', 'high')),
    source_type TEXT,
    description TEXT
);

CREATE TABLE scenarios (
    scenario_id INTEGER PRIMARY KEY,
    scenario_name TEXT NOT NULL UNIQUE,
    demand_shift REAL,
    cost_pressure REAL,
    disruption_pressure REAL,
    volatility REAL,
    scenario_probability REAL CHECK (scenario_probability >= 0 AND scenario_probability <= 1),
    description TEXT
);

CREATE TABLE scenario_scores (
    score_id INTEGER PRIMARY KEY,
    strategy_name TEXT NOT NULL,
    scenario_name TEXT NOT NULL,
    composite_score REAL NOT NULL,
    scenario_rank INTEGER,
    regret REAL,
    downside_breach INTEGER CHECK (downside_breach IN (0, 1)),
    FOREIGN KEY (strategy_name) REFERENCES strategies(strategy_name),
    FOREIGN KEY (scenario_name) REFERENCES scenarios(scenario_name)
);

CREATE TABLE thresholds (
    threshold_id INTEGER PRIMARY KEY,
    parameter_name TEXT NOT NULL,
    threshold_direction TEXT,
    threshold_value REAL,
    interpretation TEXT,
    FOREIGN KEY (parameter_name) REFERENCES parameters(parameter_name)
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
    baseline_assumptions TEXT,
    sensitivity_notes TEXT,
    scenario_notes TEXT,
    threshold_notes TEXT,
    robustness_notes TEXT,
    regret_notes TEXT,
    review_trigger TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
