-- schema_path_dependence_lock_in_decision_timing.sql
-- SQLite-compatible schema for path dependence, lock-in, and decision timing.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS scenario_performance;
DROP TABLE IF EXISTS scenarios;
DROP TABLE IF EXISTS path_scores;
DROP TABLE IF EXISTS paths;

CREATE TABLE paths (
    path_id TEXT PRIMARY KEY,
    path_name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE path_scores (
    path_id TEXT PRIMARY KEY,
    initial_value REAL,
    future_flexibility REAL,
    switching_cost REAL,
    lock_in_risk REAL,
    reversibility REAL,
    timing_sensitivity REAL,
    FOREIGN KEY (path_id) REFERENCES paths(path_id)
);

CREATE TABLE scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE scenario_performance (
    path_id TEXT,
    scenario_id TEXT,
    performance REAL,
    PRIMARY KEY (path_id, scenario_id),
    FOREIGN KEY (path_id) REFERENCES paths(path_id),
    FOREIGN KEY (scenario_id) REFERENCES scenarios(scenario_id)
);

CREATE TABLE decision_records (
    record_id TEXT PRIMARY KEY,
    decision_context TEXT NOT NULL,
    selected_action TEXT,
    rationale TEXT,
    review_trigger TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
