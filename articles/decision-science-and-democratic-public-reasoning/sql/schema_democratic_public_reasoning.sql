-- schema_democratic_public_reasoning.sql
-- SQLite-compatible schema for decision science and democratic public reasoning.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS review_triggers;
DROP TABLE IF EXISTS participation_records;
DROP TABLE IF EXISTS process_scores;
DROP TABLE IF EXISTS democratic_processes;

CREATE TABLE democratic_processes (
    process_id TEXT PRIMARY KEY,
    process_name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE process_scores (
    process_id TEXT PRIMARY KEY,
    evidence_quality REAL,
    transparency REAL,
    participation REAL,
    procedural_fairness REAL,
    contestability REAL,
    equity_review REAL,
    accountability REAL,
    uncertainty_communication REAL,
    process_burden REAL,
    public_trust_risk REAL,
    FOREIGN KEY (process_id) REFERENCES democratic_processes(process_id)
);

CREATE TABLE participation_records (
    group_id TEXT PRIMARY KEY,
    group_name TEXT NOT NULL,
    standing REAL,
    access REAL,
    participation_quality REAL,
    deliberation_quality REAL,
    response_to_input REAL,
    trust_effect REAL,
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
