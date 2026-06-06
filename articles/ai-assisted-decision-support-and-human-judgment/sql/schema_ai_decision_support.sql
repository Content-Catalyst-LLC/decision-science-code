-- schema_ai_decision_support.sql
-- SQLite-compatible schema for AI-assisted decision support and human judgment.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS review_triggers;
DROP TABLE IF EXISTS oversight_records;
DROP TABLE IF EXISTS design_scores;
DROP TABLE IF EXISTS support_designs;

CREATE TABLE support_designs (
    design_id TEXT PRIMARY KEY,
    design_name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE design_scores (
    design_id TEXT PRIMARY KEY,
    model_performance REAL,
    uncertainty_visibility REAL,
    human_oversight REAL,
    contestability REAL,
    fairness_review REAL,
    accountability REAL,
    monitoring_strength REAL,
    automation_bias_risk REAL,
    process_burden REAL,
    FOREIGN KEY (design_id) REFERENCES support_designs(design_id)
);

CREATE TABLE oversight_records (
    role_id TEXT PRIMARY KEY,
    role_name TEXT NOT NULL,
    authority REAL,
    information_access REAL,
    time_available REAL,
    training REAL,
    override_rights REAL,
    independence REAL,
    oversight_strength REAL,
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
