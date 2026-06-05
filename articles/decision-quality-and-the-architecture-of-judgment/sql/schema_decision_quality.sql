-- schema_decision_quality.sql
-- SQLite-compatible schema for decision quality and architecture of judgment workflows.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS review_triggers;
DROP TABLE IF EXISTS outcomes;
DROP TABLE IF EXISTS assumptions;
DROP TABLE IF EXISTS evidence;
DROP TABLE IF EXISTS quality_scores;
DROP TABLE IF EXISTS quality_components;
DROP TABLE IF EXISTS alternatives;

CREATE TABLE alternatives (
    alternative_id INTEGER PRIMARY KEY,
    alternative_name TEXT NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE quality_components (
    component_id INTEGER PRIMARY KEY,
    component_name TEXT NOT NULL UNIQUE,
    weight REAL NOT NULL CHECK (weight >= 0),
    description TEXT
);

CREATE TABLE quality_scores (
    score_id INTEGER PRIMARY KEY,
    alternative_id INTEGER NOT NULL,
    component_id INTEGER NOT NULL,
    score REAL NOT NULL CHECK (score >= 0 AND score <= 1),
    FOREIGN KEY (alternative_id) REFERENCES alternatives(alternative_id),
    FOREIGN KEY (component_id) REFERENCES quality_components(component_id),
    UNIQUE (alternative_id, component_id)
);

CREATE TABLE evidence (
    evidence_id INTEGER PRIMARY KEY,
    claim TEXT NOT NULL,
    evidence_type TEXT,
    quality TEXT CHECK (quality IN ('low', 'medium', 'high')),
    uncertainty_note TEXT
);

CREATE TABLE assumptions (
    assumption_id INTEGER PRIMARY KEY,
    assumption_text TEXT NOT NULL,
    confidence TEXT CHECK (confidence IN ('low', 'medium', 'high')),
    review_trigger TEXT
);

CREATE TABLE outcomes (
    outcome_id INTEGER PRIMARY KEY,
    alternative_id INTEGER NOT NULL,
    trial INTEGER,
    realized_outcome REAL,
    favorable_outcome INTEGER CHECK (favorable_outcome IN (0, 1)),
    FOREIGN KEY (alternative_id) REFERENCES alternatives(alternative_id)
);

CREATE TABLE review_triggers (
    trigger_id INTEGER PRIMARY KEY,
    trigger_name TEXT NOT NULL UNIQUE,
    threshold REAL,
    interpretation TEXT
);

CREATE TABLE decision_records (
    record_id INTEGER PRIMARY KEY,
    decision_context TEXT NOT NULL,
    selected_alternative TEXT,
    decision_quality_score REAL,
    outcome_quality TEXT,
    rationale TEXT,
    review_trigger TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
