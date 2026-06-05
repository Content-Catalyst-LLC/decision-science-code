-- schema_core_principles_decisions.sql
-- SQLite-compatible schema for core-principles decision workflows.

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS decision_records;
DROP TABLE IF EXISTS model_runs;
DROP TABLE IF EXISTS evidence;
DROP TABLE IF EXISTS assumptions;
DROP TABLE IF EXISTS scenario_results;
DROP TABLE IF EXISTS scenarios;
DROP TABLE IF EXISTS principle_scores;
DROP TABLE IF EXISTS criteria;
DROP TABLE IF EXISTS alternatives;

CREATE TABLE alternatives (
    alternative_id INTEGER PRIMARY KEY,
    alternative_name TEXT NOT NULL UNIQUE,
    description TEXT
);

CREATE TABLE criteria (
    criterion_id INTEGER PRIMARY KEY,
    criterion_name TEXT NOT NULL UNIQUE,
    weight REAL NOT NULL CHECK (weight >= 0),
    description TEXT
);

CREATE TABLE principle_scores (
    score_id INTEGER PRIMARY KEY,
    alternative_id INTEGER NOT NULL,
    criterion_id INTEGER NOT NULL,
    score REAL NOT NULL CHECK (score >= 0 AND score <= 1),
    FOREIGN KEY (alternative_id) REFERENCES alternatives(alternative_id),
    FOREIGN KEY (criterion_id) REFERENCES criteria(criterion_id),
    UNIQUE (alternative_id, criterion_id)
);

CREATE TABLE scenarios (
    scenario_id INTEGER PRIMARY KEY,
    scenario_name TEXT NOT NULL UNIQUE,
    probability REAL CHECK (probability >= 0 AND probability <= 1),
    system_stress REAL,
    learning_opportunity REAL
);

CREATE TABLE scenario_results (
    result_id INTEGER PRIMARY KEY,
    alternative_id INTEGER NOT NULL,
    scenario_id INTEGER NOT NULL,
    outcome_value REAL,
    robustness_pass INTEGER CHECK (robustness_pass IN (0, 1)),
    FOREIGN KEY (alternative_id) REFERENCES alternatives(alternative_id),
    FOREIGN KEY (scenario_id) REFERENCES scenarios(scenario_id)
);

CREATE TABLE assumptions (
    assumption_id INTEGER PRIMARY KEY,
    assumption_text TEXT NOT NULL,
    category TEXT,
    confidence TEXT CHECK (confidence IN ('low', 'medium', 'high')),
    review_trigger TEXT
);

CREATE TABLE evidence (
    evidence_id INTEGER PRIMARY KEY,
    claim TEXT NOT NULL,
    evidence_type TEXT,
    quality TEXT CHECK (quality IN ('low', 'medium', 'high')),
    notes TEXT
);

CREATE TABLE model_runs (
    run_id INTEGER PRIMARY KEY,
    workflow_name TEXT NOT NULL,
    language TEXT NOT NULL,
    run_timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL
);

CREATE TABLE decision_records (
    record_id INTEGER PRIMARY KEY,
    decision_context TEXT NOT NULL,
    selected_alternative TEXT,
    rationale TEXT,
    review_trigger TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
);
