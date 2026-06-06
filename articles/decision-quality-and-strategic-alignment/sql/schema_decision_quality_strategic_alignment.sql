-- schema_decision_quality_strategic_alignment.sql
-- SQLite-compatible schema for decision quality and strategic alignment.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS review_triggers;
DROP TABLE IF EXISTS strategy_vectors;
DROP TABLE IF EXISTS alignment_dimensions;
DROP TABLE IF EXISTS quality_dimensions;
DROP TABLE IF EXISTS decisions;

CREATE TABLE decisions (
    decision_id TEXT PRIMARY KEY,
    decision_name TEXT NOT NULL,
    objective_clarity REAL,
    alternative_quality REAL,
    information_strength REAL,
    tradeoff_transparency REAL,
    uncertainty_treatment REAL,
    implementation_readiness REAL,
    strategic_fit REAL,
    capability_fit REAL,
    value_fit REAL
);

CREATE TABLE quality_dimensions (
    dimension_id TEXT PRIMARY KEY,
    dimension_name TEXT NOT NULL,
    weight REAL CHECK (weight >= 0),
    description TEXT
);

CREATE TABLE alignment_dimensions (
    dimension_id TEXT PRIMARY KEY,
    dimension_name TEXT NOT NULL,
    weight REAL CHECK (weight >= 0),
    description TEXT
);

CREATE TABLE strategy_vectors (
    dimension_name TEXT PRIMARY KEY,
    weight REAL CHECK (weight >= 0)
);

CREATE TABLE review_triggers (
    trigger_id TEXT PRIMARY KEY,
    indicator TEXT NOT NULL,
    threshold_direction TEXT NOT NULL,
    threshold_value REAL,
    review_owner TEXT
);

CREATE TABLE decision_records (
    record_id TEXT PRIMARY KEY,
    decision_context TEXT NOT NULL,
    selected_action TEXT,
    rationale TEXT,
    review_trigger TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
