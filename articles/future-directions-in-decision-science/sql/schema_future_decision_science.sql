-- schema_future_decision_science.sql
-- SQLite-compatible schema for future directions in decision science.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS review_triggers;
DROP TABLE IF EXISTS maturity_records;
DROP TABLE IF EXISTS pathway_scores;
DROP TABLE IF EXISTS future_pathways;

CREATE TABLE future_pathways (
    pathway_id TEXT PRIMARY KEY,
    pathway_name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE pathway_scores (
    pathway_id TEXT PRIMARY KEY,
    ai_readiness REAL,
    governance_maturity REAL,
    uncertainty_capability REAL,
    participatory_legitimacy REAL,
    reproducibility REAL,
    systems_modeling REAL,
    ethical_accountability REAL,
    adaptive_capacity REAL,
    process_burden REAL,
    failure_risk REAL,
    FOREIGN KEY (pathway_id) REFERENCES future_pathways(pathway_id)
);

CREATE TABLE maturity_records (
    dimension_id TEXT PRIMARY KEY,
    dimension_name TEXT NOT NULL,
    current_maturity REAL,
    target_maturity REAL,
    gap REAL,
    priority TEXT,
    notes TEXT
);

CREATE TABLE review_triggers (
    trigger_id TEXT PRIMARY KEY,
    trigger_name TEXT NOT NULL,
    trigger_value REAL,
    description TEXT
);

CREATE TABLE decision_records (
    record_id TEXT PRIMARY KEY,
    decision_context TEXT NOT NULL,
    selected_action TEXT,
    rationale TEXT,
    review_trigger TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
