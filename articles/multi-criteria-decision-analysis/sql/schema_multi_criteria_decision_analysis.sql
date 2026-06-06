-- schema_multi_criteria_decision_analysis.sql
-- SQLite-compatible schema for Multi-Criteria Decision Analysis.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS rankings;
DROP TABLE IF EXISTS weights;
DROP TABLE IF EXISTS scores;
DROP TABLE IF EXISTS criteria;
DROP TABLE IF EXISTS alternatives;

CREATE TABLE alternatives (
    alternative_id TEXT PRIMARY KEY,
    alternative_name TEXT NOT NULL,
    description TEXT
);

CREATE TABLE criteria (
    criterion_id TEXT PRIMARY KEY,
    criterion_name TEXT NOT NULL,
    direction TEXT CHECK (direction IN ('benefit', 'cost')),
    description TEXT
);

CREATE TABLE scores (
    alternative_id TEXT,
    criterion_id TEXT,
    raw_score REAL,
    normalized_score REAL,
    evidence_quality TEXT,
    PRIMARY KEY (alternative_id, criterion_id),
    FOREIGN KEY (alternative_id) REFERENCES alternatives(alternative_id),
    FOREIGN KEY (criterion_id) REFERENCES criteria(criterion_id)
);

CREATE TABLE weights (
    profile_name TEXT,
    criterion_id TEXT,
    weight REAL CHECK (weight >= 0),
    PRIMARY KEY (profile_name, criterion_id),
    FOREIGN KEY (criterion_id) REFERENCES criteria(criterion_id)
);

CREATE TABLE rankings (
    profile_name TEXT,
    alternative_id TEXT,
    composite_score REAL,
    rank INTEGER,
    PRIMARY KEY (profile_name, alternative_id),
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
