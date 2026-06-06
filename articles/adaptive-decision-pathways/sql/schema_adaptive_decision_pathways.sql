-- schema_adaptive_decision_pathways.sql
-- SQLite-compatible schema for adaptive decision pathways.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS scenario_performance;
DROP TABLE IF EXISTS pathway_scores;
DROP TABLE IF EXISTS pathways;
DROP TABLE IF EXISTS scenarios;

CREATE TABLE pathways (
    pathway_id TEXT PRIMARY KEY,
    pathway_name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE pathway_scores (
    pathway_id TEXT PRIMARY KEY,
    initial_performance REAL,
    flexibility REAL,
    monitoring_quality REAL,
    trigger_clarity REAL,
    switching_cost REAL,
    fallback_strength REAL,
    FOREIGN KEY (pathway_id) REFERENCES pathways(pathway_id)
);

CREATE TABLE scenarios (
    scenario_id TEXT PRIMARY KEY,
    scenario_name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE scenario_performance (
    pathway_id TEXT,
    scenario_id TEXT,
    performance REAL,
    PRIMARY KEY (pathway_id, scenario_id),
    FOREIGN KEY (pathway_id) REFERENCES pathways(pathway_id),
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
