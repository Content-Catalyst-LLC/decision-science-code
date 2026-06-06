-- schema_decision_governance_accountability.sql
-- SQLite-compatible schema for decision governance and institutional accountability.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS review_triggers;
DROP TABLE IF EXISTS accountability_records;
DROP TABLE IF EXISTS governance_scores;
DROP TABLE IF EXISTS governance_designs;

CREATE TABLE governance_designs (
    design_id TEXT PRIMARY KEY,
    design_name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE governance_scores (
    design_id TEXT PRIMARY KEY,
    decision_quality REAL,
    legitimacy REAL,
    accountability REAL,
    implementation_reliability REAL,
    evidence_traceability REAL,
    review_strength REAL,
    monitoring_strength REAL,
    corrective_capacity REAL,
    risk_exposure REAL,
    process_burden REAL,
    FOREIGN KEY (design_id) REFERENCES governance_designs(design_id)
);

CREATE TABLE accountability_records (
    actor_id TEXT PRIMARY KEY,
    actor_name TEXT NOT NULL,
    decision_influence REAL,
    accountability REAL,
    role_name TEXT,
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
