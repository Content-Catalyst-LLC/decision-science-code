-- schema_decision_records.sql
-- SQLite-compatible schema for decision records and accountable judgment.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS review_triggers;
DROP TABLE IF EXISTS dissent;
DROP TABLE IF EXISTS assumptions;
DROP TABLE IF EXISTS evidence;
DROP TABLE IF EXISTS alternatives;
DROP TABLE IF EXISTS decisions;

CREATE TABLE decisions (
    decision_id INTEGER PRIMARY KEY,
    record_id TEXT NOT NULL UNIQUE,
    decision_context TEXT NOT NULL,
    decision_owner TEXT,
    recommendation_owner TEXT,
    decision_date TEXT,
    selected_action TEXT,
    rationale TEXT
);

CREATE TABLE alternatives (
    alternative_id INTEGER PRIMARY KEY,
    record_id TEXT NOT NULL,
    alternative_name TEXT NOT NULL,
    status TEXT CHECK (status IN ('selected', 'rejected', 'deferred', 'staged')),
    reason TEXT,
    reconsideration_condition TEXT,
    FOREIGN KEY (record_id) REFERENCES decisions(record_id)
);

CREATE TABLE evidence (
    evidence_id INTEGER PRIMARY KEY,
    record_id TEXT NOT NULL,
    claim TEXT NOT NULL,
    evidence_type TEXT,
    evidence_quality REAL CHECK (evidence_quality >= 0 AND evidence_quality <= 1),
    evidence_linked INTEGER CHECK (evidence_linked IN (0, 1)),
    uncertainty_note TEXT,
    FOREIGN KEY (record_id) REFERENCES decisions(record_id)
);

CREATE TABLE assumptions (
    assumption_id INTEGER PRIMARY KEY,
    record_id TEXT NOT NULL,
    assumption_text TEXT NOT NULL,
    confidence REAL CHECK (confidence >= 0 AND confidence <= 1),
    criticality REAL CHECK (criticality >= 0 AND criticality <= 1),
    monitored INTEGER CHECK (monitored IN (0, 1)),
    FOREIGN KEY (record_id) REFERENCES decisions(record_id)
);

CREATE TABLE dissent (
    dissent_id INTEGER PRIMARY KEY,
    record_id TEXT NOT NULL,
    dissent_type TEXT,
    dissent_summary TEXT,
    response TEXT,
    unresolved INTEGER CHECK (unresolved IN (0, 1)),
    FOREIGN KEY (record_id) REFERENCES decisions(record_id)
);

CREATE TABLE review_triggers (
    trigger_id INTEGER PRIMARY KEY,
    record_id TEXT NOT NULL,
    indicator TEXT NOT NULL,
    lower_bound REAL,
    upper_bound REAL,
    current_value REAL,
    review_owner TEXT,
    active INTEGER CHECK (active IN (0, 1)),
    FOREIGN KEY (record_id) REFERENCES decisions(record_id)
);

CREATE TABLE decision_records (
    audit_id INTEGER PRIMARY KEY,
    record_id TEXT NOT NULL,
    accountable_judgment_score REAL,
    traceability_share REAL,
    assumption_risk REAL,
    review_priority TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (record_id) REFERENCES decisions(record_id)
);
