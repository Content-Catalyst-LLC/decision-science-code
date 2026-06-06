-- schema_stakeholder_values_decision_legitimacy.sql
-- SQLite-compatible schema for stakeholder values and decision legitimacy.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS procedure_scores;
DROP TABLE IF EXISTS burdens;
DROP TABLE IF EXISTS value_weights;
DROP TABLE IF EXISTS alternatives;
DROP TABLE IF EXISTS criteria;
DROP TABLE IF EXISTS stakeholders;

CREATE TABLE stakeholders (
    stakeholder_id TEXT PRIMARY KEY,
    stakeholder_name TEXT NOT NULL,
    importance REAL,
    minimum_threshold REAL,
    description TEXT
);

CREATE TABLE criteria (
    criterion_id TEXT PRIMARY KEY,
    criterion_name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE alternatives (
    alternative_id TEXT PRIMARY KEY,
    alternative_name TEXT NOT NULL,
    cost_efficiency REAL,
    service_quality REAL,
    equity REAL,
    autonomy REAL,
    resilience REAL,
    transparency REAL
);

CREATE TABLE value_weights (
    stakeholder_id TEXT,
    criterion_id TEXT,
    weight REAL,
    PRIMARY KEY (stakeholder_id, criterion_id),
    FOREIGN KEY (stakeholder_id) REFERENCES stakeholders(stakeholder_id),
    FOREIGN KEY (criterion_id) REFERENCES criteria(criterion_id)
);

CREATE TABLE burdens (
    alternative_id TEXT,
    stakeholder_id TEXT,
    burden REAL,
    PRIMARY KEY (alternative_id, stakeholder_id),
    FOREIGN KEY (alternative_id) REFERENCES alternatives(alternative_id),
    FOREIGN KEY (stakeholder_id) REFERENCES stakeholders(stakeholder_id)
);

CREATE TABLE procedure_scores (
    alternative_id TEXT PRIMARY KEY,
    voice REAL,
    transparency REAL,
    explanation REAL,
    contestability REAL,
    review REAL,
    FOREIGN KEY (alternative_id) REFERENCES alternatives(alternative_id)
);

CREATE TABLE decision_records (
    record_id TEXT PRIMARY KEY,
    decision_context TEXT NOT NULL,
    selected_action TEXT,
    rationale TEXT,
    review_trigger TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
